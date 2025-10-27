int login(void) {
    char username[50], password[50];
    printf("Enter Username: ");
    scanf("%s", username);
    printf("Enter Password: ");
    scanf("%s", password);

    if (strcmp(username, ADMIN_USERNAME) == 0 && strcmp(password, ADMIN_PASSWORD) == 0) {
        printf("Login successful!\n");
        return 1;
    }
    printf("Invalid credentials. Try again.\n");
    return 0;
}
