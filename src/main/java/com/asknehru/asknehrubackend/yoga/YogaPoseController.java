package com.asknehru.asknehrubackend.yoga;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/yoga/poses")
@CrossOrigin(origins = "*")
public class YogaPoseController {
    
    private final YogaPoseService yogaPoseService;
    
    public YogaPoseController(YogaPoseService yogaPoseService) {
        this.yogaPoseService = yogaPoseService;
    }
    
    @GetMapping
    public ResponseEntity<List<YogaPose>> getAllPoses() {
        return ResponseEntity.ok(yogaPoseService.getAllPoses());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<YogaPose> getPoseById(@PathVariable Long id) {
        return ResponseEntity.ok(yogaPoseService.getPoseById(id));
    }
    
    @GetMapping("/search")
    public ResponseEntity<List<YogaPose>> searchPoses(@RequestParam String yogaName) {
        return ResponseEntity.ok(yogaPoseService.searchPosesByYogaName(yogaName));
    }
    
    @PostMapping
    public ResponseEntity<YogaPose> createPose(@RequestBody YogaPose yogaPose) {
        YogaPose created = yogaPoseService.createPose(yogaPose);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<YogaPose> updatePose(@PathVariable Long id, @RequestBody YogaPose yogaPose) {
        return ResponseEntity.ok(yogaPoseService.updatePose(id, yogaPose));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePose(@PathVariable Long id) {
        yogaPoseService.deletePose(id);
        return ResponseEntity.noContent().build();
    }
    
    @ExceptionHandler(YogaPoseNotFoundException.class)
    public ResponseEntity<String> handleNotFound(YogaPoseNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }
}
