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
