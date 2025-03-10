USE project;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    task TEXT NOT NULL,
    deadline DATE NOT NULL,
    priority ENUM('High', 'Medium', 'Low') NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
