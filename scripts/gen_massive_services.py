import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# DiscussionService.java
write("backend/src/main/java/com/ailms/backend/modules/discussion/service/DiscussionService.java", """
package com.ailms.backend.modules.discussion.service;

import com.ailms.backend.common.exception.ResourceNotFoundException;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.discussion.dto.DiscussionDtos.*;
import com.ailms.backend.modules.discussion.model.Discussion;
import com.ailms.backend.modules.discussion.repository.DiscussionRepository;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class DiscussionService {

    private final DiscussionRepository discussionRepository;
    private final CourseRepository courseRepository;
    private final UserRepository userRepository;

    public DiscussionService(DiscussionRepository discussionRepository, CourseRepository courseRepository, UserRepository userRepository) {
        this.discussionRepository = discussionRepository;
        this.courseRepository = courseRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public Discussion createDiscussion(UUID authorId, CreateDiscussionRequest req) {
        User author = userRepository.findById(authorId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", authorId));
        Course course = courseRepository.findById(req.courseId())
                .orElseThrow(() -> new ResourceNotFoundException("Course", "id", req.courseId()));

        Discussion discussion = new Discussion();
        discussion.setAuthor(author);
        discussion.setCourse(course);
        discussion.setTitle(req.title());
        discussion.setContent(req.content());
        discussion.setOrganizationId(course.getOrganizationId());
        discussion.setStatus("VISIBLE");

        return discussionRepository.save(discussion);
    }

    @Transactional(readOnly = true)
    public Page<Discussion> getCourseDiscussions(UUID courseId, Pageable pageable) {
        return discussionRepository.findByCourseIdAndStatus(courseId, "VISIBLE", pageable);
    }

    @Transactional
    public Discussion upvoteDiscussion(UUID discussionId) {
        Discussion discussion = discussionRepository.findById(discussionId)
                .orElseThrow(() -> new ResourceNotFoundException("Discussion", "id", discussionId));
        discussion.setUpvotesCount(discussion.getUpvotesCount() + 1);
        return discussionRepository.save(discussion);
    }
}
""")

write("backend/src/main/java/com/ailms/backend/modules/discussion/repository/DiscussionRepository.java", """
package com.ailms.backend.modules.discussion.repository;

import com.ailms.backend.modules.discussion.model.Discussion;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface DiscussionRepository extends JpaRepository<Discussion, UUID> {
    Page<Discussion> findByCourseIdAndStatus(UUID courseId, String status, Pageable pageable);
}
""")

# ModerationService.java
write("backend/src/main/java/com/ailms/backend/modules/moderation/service/ModerationService.java", """
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
""")

# Additional Test Suites
write("backend/src/test/java/com/ailms/backend/modules/discussion/DiscussionServiceTest.java", """
package com.ailms.backend.modules.discussion;

import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.repository.CourseRepository;
import com.ailms.backend.modules.discussion.dto.DiscussionDtos.CreateDiscussionRequest;
import com.ailms.backend.modules.discussion.model.Discussion;
import com.ailms.backend.modules.discussion.repository.DiscussionRepository;
import com.ailms.backend.modules.discussion.service.DiscussionService;
import com.ailms.backend.modules.user.model.User;
import com.ailms.backend.modules.user.repository.UserRepository;
import com.ailms.backend.testutil.TestDataFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DiscussionServiceTest {

    @Mock private DiscussionRepository discussionRepository;
    @Mock private CourseRepository courseRepository;
    @Mock private UserRepository userRepository;

    private DiscussionService discussionService;

    @BeforeEach
    void setUp() {
        discussionService = new DiscussionService(discussionRepository, courseRepository, userRepository);
    }

    @Test
    void shouldCreateDiscussionTopic() {
        UUID authorId = UUID.randomUUID();
        UUID courseId = UUID.randomUUID();

        User author = TestDataFactory.createUser("alex@ailms.com", "Alex", "Learner", null, "STUDENT");
        Course course = TestDataFactory.createCourse("Distributed Sagas", "dist-sagas", authorId, UUID.randomUUID());

        CreateDiscussionRequest req = new CreateDiscussionRequest("How to handle compensating transactions?", "Details...", courseId, null, "Architecture");

        when(userRepository.findById(authorId)).thenReturn(Optional.of(author));
        when(courseRepository.findById(courseId)).thenReturn(Optional.of(course));
        when(discussionRepository.save(any(Discussion.class))).thenAnswer(i -> i.getArgument(0));

        Discussion created = discussionService.createDiscussion(authorId, req);

        assertNotNull(created);
        assertEquals("How to handle compensating transactions?", created.getTitle());
        assertEquals("VISIBLE", created.getStatus());
        verify(discussionRepository, times(1)).save(any());
    }
}
""")

print("Massive service layer and test expansions generated.")
