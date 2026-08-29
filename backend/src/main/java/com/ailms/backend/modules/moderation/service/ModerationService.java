package com.ailms.backend.modules.moderation.service;

import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.discussion.dto.DiscussionDtos.CreateReportRequest;
import com.ailms.backend.modules.discussion.model.Discussion;
import com.ailms.backend.modules.discussion.repository.DiscussionRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class ModerationService {

    private final DiscussionRepository discussionRepository;

    public ModerationService(DiscussionRepository discussionRepository) {
        this.discussionRepository = discussionRepository;
    }

    @Transactional
    public void flagContent(CreateReportRequest report, UUID reporterId) {
        if ("DISCUSSION".equalsIgnoreCase(report.targetEntityType())) {
            Discussion discussion = discussionRepository.findById(report.targetEntityId())
                    .orElseThrow(() -> new ResourceNotFoundException("Discussion", "id", report.targetEntityId()));
            discussion.setStatus("FLAGGED");
            discussionRepository.save(discussion);
        }
    }

    @Transactional
    public void resolveReport(UUID entityId, String entityType, boolean hideContent, UUID moderatorId) {
        if ("DISCUSSION".equalsIgnoreCase(entityType)) {
            Discussion discussion = discussionRepository.findById(entityId)
                    .orElseThrow(() -> new ResourceNotFoundException("Discussion", "id", entityId));
            discussion.setStatus(hideContent ? "HIDDEN" : "VISIBLE");
            discussionRepository.save(discussion);
        }
    }
}
