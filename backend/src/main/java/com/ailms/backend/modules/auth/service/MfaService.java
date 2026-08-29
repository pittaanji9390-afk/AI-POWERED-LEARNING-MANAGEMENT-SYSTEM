package com.ailms.backend.modules.auth.service;

import com.ailms.backend.common.exception.BadRequestException;
import org.springframework.stereotype.Service;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.ByteBuffer;
import java.security.SecureRandom;
import java.util.*;

@Service
public class MfaService {

    private static final String BASE32_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    private static final SecureRandom RANDOM = new SecureRandom();

    public String generateMfaSecret() {
        byte[] buffer = new byte[20];
        RANDOM.nextBytes(buffer);
        StringBuilder secret = new StringBuilder(32);
        for (byte b : buffer) {
            secret.append(BASE32_CHARS.charAt((b & 0xFF) % BASE32_CHARS.length()));
        }
        return secret.toString();
    }

    public List<String> generateRecoveryCodes(int count) {
        List<String> codes = new ArrayList<>(count);
        for (int i = 0; i < count; i++) {
            StringBuilder code = new StringBuilder();
            for (int j = 0; j < 10; j++) {
                if (j == 5) code.append("-");
                code.append(Integer.toHexString(RANDOM.nextInt(16)).toUpperCase());
            }
            codes.add(code.toString());
        }
        return codes;
    }

    public boolean verifyTotpCode(String secret, int inputCode) {
        long currentInterval = System.currentTimeMillis() / 1000 / 30;
        // Verify current window +- 1 interval (clock drift tolerance)
        for (int i = -1; i <= 1; i++) {
            if (generateTotp(secret, currentInterval + i) == inputCode) {
                return true;
            }
        }
        return false;
    }

    private int generateTotp(String secret, long timeInterval) {
        try {
            byte[] key = decodeBase32(secret);
            byte[] data = ByteBuffer.allocate(8).putLong(timeInterval).array();
            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(new SecretKeySpec(key, "HmacSHA1"));
            byte[] hash = mac.doFinal(data);

            int offset = hash[hash.length - 1] & 0x0F;
            int binary = ((hash[offset] & 0x7F) << 24)
                    | ((hash[offset + 1] & 0xFF) << 16)
                    | ((hash[offset + 2] & 0xFF) << 8)
                    | (hash[offset + 3] & 0xFF);

            return binary % 1_000_000;
        } catch (Exception e) {
            throw new BadRequestException("Failed to verify TOTP code: " + e.getMessage());
        }
    }

    private byte[] decodeBase32(String secret) {
        byte[] bytes = new byte[secret.length() * 5 / 8];
        int buffer = 0;
        int bitsLeft = 0;
        int count = 0;

        for (char c : secret.toUpperCase().toCharArray()) {
            int val = BASE32_CHARS.indexOf(c);
            if (val < 0) continue;
            buffer = (buffer << 5) | val;
            bitsLeft += 5;
            if (bitsLeft >= 8) {
                bytes[count++] = (byte) ((buffer >> (bitsLeft - 8)) & 0xFF);
                bitsLeft -= 8;
            }
        }
        return bytes;
    }
}
