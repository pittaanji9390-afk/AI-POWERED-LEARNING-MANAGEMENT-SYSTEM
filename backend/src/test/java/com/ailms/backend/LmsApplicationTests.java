package com.ailms.backend;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
@ActiveProfiles("dev")
class LmsApplicationTests {

    @Test
    void contextLoads() {
        assertTrue(true, "Application context baseline test passed");
    }
}
