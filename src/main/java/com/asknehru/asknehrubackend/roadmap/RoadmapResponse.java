package com.asknehru.asknehrubackend.roadmap;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RoadmapResponse {
    private Long id;
    private String mainTopic;
    private String syllabus;
    private String imageUrl;
    private String routerLink;
    private String intro;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
