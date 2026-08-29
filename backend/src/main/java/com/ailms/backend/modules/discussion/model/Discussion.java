package com.ailms.backend.modules.discussion.model;

import com.ailms.backend.common.domain.TenantAwareEntity;
import com.ailms.backend.modules.course.model.Course;
import com.ailms.backend.modules.course.model.Lesson;
import com.ailms.backend.modules.user.model.User;
import jakarta.persistence.*;

@Entity
@Table(name = "discussions")
public class Discussion extends TenantAwareEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "course_id", nullable = false)
    private Course course;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lesson_id")
    private Lesson lesson;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(name = "title", nullable = false)
    private String title;

    @Column(name = "content", nullable = false, columnDefinition = "TEXT")
    private String content;

    @Column(name = "is_pinned")
    private Boolean isPinned = false;

    @Column(name = "is_locked")
    private Boolean isLocked = false;

    @Column(name = "upvotes_count")
    private Integer upvotesCount = 0;

    @Column(name = "comments_count")
    private Integer commentsCount = 0;

    @Column(name = "status")
    private String status = "VISIBLE";

    public Course getCourse() { return course; }
    public void setCourse(Course course) { this.course = course; }
    public Lesson getLesson() { return lesson; }
    public void setLesson(Lesson lesson) { this.lesson = lesson; }
    public User getAuthor() { return author; }
    public void setAuthor(User author) { this.author = author; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public Boolean getIsPinned() { return isPinned; }
    public void setIsPinned(Boolean isPinned) { this.isPinned = isPinned; }
    public Boolean getIsLocked() { return isLocked; }
    public void setIsLocked(Boolean isLocked) { this.isLocked = isLocked; }
    public Integer getUpvotesCount() { return upvotesCount; }
    public void setUpvotesCount(Integer upvotesCount) { this.upvotesCount = upvotesCount; }
    public Integer getCommentsCount() { return commentsCount; }
    public void setCommentsCount(Integer commentsCount) { this.commentsCount = commentsCount; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
