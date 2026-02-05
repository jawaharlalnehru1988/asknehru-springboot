package com.asknehru.demoapp.users;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<UserAccount, Long> {
    boolean existsByUsernameIgnoreCase(String username);
    boolean existsByEmailIgnoreCase(String email);
	java.util.Optional<UserAccount> findByUsernameIgnoreCase(String username);
	java.util.Optional<UserAccount> findByEmailIgnoreCase(String email);
}
