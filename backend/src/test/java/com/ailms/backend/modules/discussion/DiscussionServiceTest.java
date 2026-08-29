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
