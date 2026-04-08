package uz.marketly.identity;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class IdentityController {

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("service", "identity-profile-java", "status", "ok");
    }

    @PostMapping("/api/v1/auth/login")
    public Map<String, Object> login(@RequestBody Map<String, Object> body) {
        return Map.of(
            "service", "identity-profile-java",
            "message", "Marketly auth/profile service scaffold",
            "payload", body
        );
    }
}
