package com.ailms.backend.common.event.listener;

import com.ailms.backend.common.event.LearningEvent;
import com.ailms.backend.modules.certificate.service.CertificateService;
import com.ailms.backend.modules.notification.service.NotificationDispatcherService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
public class LearningEventListener {

    private static final Logger log = LoggerFactory.getLogger(LearningEventListener.class);

    private final NotificationDispatcherService notificationDispatcher;
    private final CertificateService certificateService;

    public LearningEventListener(NotificationDispatcherService notificationDispatcher, CertificateService certificateService) {
        this.notificationDispatcher = notificationDispatcher;
        this.certificateService = certificateService;
    }

    @Async("eventTaskExecutor")
    @EventListener
    public void handleLearningEvent(LearningEvent event) {
        log.info("Processing asynchronous domain event: [type={}, studentId={}, courseId={}]",
                event.getEventType(), event.getStudentId(), event.getCourseId());

        switch (event.getEventType()) {
            case "LESSON_COMPLETED" -> {
                notificationDispatcher.dispatch(
                        event.getStudentId(),
                        "Lesson Milestone Achieved",
                        "Great job! You completed a lesson. Keep your learning momentum going!",
                        "MILESTONE",
                        "/my-learning"
                );
            }
            case "COURSE_COMPLETED" -> {
                log.info("Triggering automatic certificate issuance for learner {}", event.getStudentId());
                try {
                    certificateService.issueCertificate(event.getStudentId(), event.getCourseId());
                    notificationDispatcher.dispatch(
                            event.getStudentId(),
                            "Course Completed & Certificate Issued!",
                            "Congratulations! You completed the course and your verified certificate is now ready.",
                            "CERTIFICATE",
                            "/certificates"
                    );
                } catch (Exception e) {
                    log.warn("Certificate already issued or handling duplicate event: {}", e.getMessage());
                }
            }
        }
    }
}
