package com.asknehru.asknehrubackend.roadmap;

import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RoadmapUpdateRequest {
    @Size(max = 200, message = "Main topic must not exceed 200 characters")
    private String mainTopic;

    private String syllabus;

    private String routerLink;

    @Size(max = 100, message = "Intro must not exceed 100 characters")
    private String intro;
}
