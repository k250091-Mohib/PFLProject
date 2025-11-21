#include <stdio.h>
#include <limits.h>
#include <string.h>

// Predefined admin credentials
#define ADMIN_USERNAME "admin"
#define ADMIN_PASSWORD "Fast1234"

#define MAX_ITEMS 50

typedef struct Item {
    int id;
    char name[50];
    int quantity;
    float price;
    int soldCount;
    int isDeleted; // Flag to mark if the item is deleted
} Item;

int Income[MAX_ITEMS];

Item inventory[MAX_ITEMS];
int itemCount = 0;

// Function Prototypes
int login(void);
void displayMenu(void);
void addItem(int id, char* name, int quantity, float price);
Item* searchItemByID(int id);
void saveInventoryToFile(void);
void loadInventoryFromFile(void);
void trackSoldItems(void);
void RemoveItem(void);
int revenue_Check(int arr[]);
void sellItem(int id, int quantitySold);
void restock(void);
void displayInventory(void);

// Function Definitions

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

void displayMenu(void) {
    printf("\n--- Inventory Management System ---\n");
    printf("1. Add Item\n");
    printf("2. Sell Item\n");
    printf("3. Display Inventory\n");
    printf("4. Restock Item\n");
    printf("5. Check Revenue\n");
    printf("6. Remove Item\n");
    printf("7. Search Item by ID\n");
    printf("8. Track Most and Least Sold Items\n");
    printf("9. Save Inventory\n");
    printf("10. Exit\n");
}

void addItem(int id, char* name, int quantity, float price) {
    if (itemCount < MAX_ITEMS) {
        inventory[itemCount].id = id;
        strncpy(inventory[itemCount].name, name, 50);
        inventory[itemCount].quantity = quantity;
        inventory[itemCount].price = price;
        inventory[itemCount].soldCount = 0;
        inventory[itemCount].isDeleted = 0;
        itemCount++;
        printf("Item added successfully: %s\n", name);
    } else {
        printf("Inventory full. Cannot add more items.\n");
    }
}

Item* searchItemByID(int id) {
    for (int i = 0; i < itemCount; i++) {
        if (inventory[i].id == id && !inventory[i].isDeleted) {
            return &inventory[i];
        }
    }
    return NULL;
}

void saveInventoryToFile(void) {
    FILE *file = fopen("inventory.txt", "w");
    if (file == NULL) {
        printf("Unable to open file for writing.\n");
        return;
    }

    fprintf(file, "%d\n", itemCount);
    for (int i = 0; i < itemCount; i++) {
        if (!inventory[i].isDeleted) {
            fprintf(file, "%d,%s,%d,%.2f,%d\n", 
                    inventory[i].id, 
                    inventory[i].name, 
                    inventory[i].quantity, 
                    inventory[i].price, 
                    inventory[i].soldCount);
        }
    }

    for (int i = 0; i < itemCount; i++) {
        fprintf(file, "%d,", Income[i]);
    }
    fprintf(file, "\n");

    fclose(file);
    printf("Inventory and income saved successfully.\n");
}

void loadInventoryFromFile(void) {
    FILE *file = fopen("inventory.txt", "r");
    if (file == NULL) {
        printf("Unable to open file for reading.\n");
        return;
    }

    if (fscanf(file, "%d\n", &itemCount) != 1) {
        printf("Error reading item count from file.\n");
        fclose(file);
        return;
    }

    for (int i = 0; i < itemCount; i++) {
        if (fscanf(file, "%d,%49[^,],%d,%f,%d\n", 
               &inventory[i].id, 
               inventory[i].name, 
               &inventory[i].quantity, 
               &inventory[i].price, 
               &inventory[i].soldCount) != 5) {
            printf("Error reading item %d from file.\n", i + 1);
            fclose(file);
            return;
        }
        inventory[i].isDeleted = 0;
    }

    for (int i = 0; i < itemCount; i++) {
        if (fscanf(file, "%d,", &Income[i]) != 1) {
            printf("Error reading income data for item %d.\n", i + 1);
            fclose(file);
            return;
        }
    }
    fscanf(file, "\n");

    fclose(file);
    printf("Inventory and income loaded successfully.\n");
}

void trackSoldItems(void) {
    if (itemCount == 0) {
        printf("No items in inventory to analyze.\n");
        return;
    }

    int maxSold = 0, minSold = INT_MAX;
    int hasSoldItems = 0;

    for (int i = 0; i < itemCount; i++) {
        if (inventory[i].isDeleted) continue;

        hasSoldItems = 1;
        if (inventory[i].soldCount > maxSold) {
            maxSold = inventory[i].soldCount;
        }
        if (inventory[i].soldCount < minSold) {
            minSold = inventory[i].soldCount;
        }
    }

    if (!hasSoldItems) {
        printf("No items to analyze (all are deleted).\n");
        return;
    }

    printf("\n--- Sales Report ---\n");

    printf("Most Sold Item(s):\n");
    for (int i = 0; i < itemCount; i++) {
        if (!inventory[i].isDeleted && inventory[i].soldCount == maxSold) {
            printf("ID: %d, Name: %s, Quantity Sold: %d\n", 
                   inventory[i].id, inventory[i].name, inventory[i].soldCount);
        }
    }

    printf("\nLeast Sold Item(s):\n");
    for (int i = 0; i < itemCount; i++) {
        if (!inventory[i].isDeleted && inventory[i].soldCount == minSold) {
            printf("ID: %d, Name: %s, Quantity Sold: %d\n", 
                   inventory[i].id, inventory[i].name, inventory[i].soldCount);
        }
    }
}

void RemoveItem(void) {
    int num_id;
    printf("Enter the id of the item you want to remove: ");
    scanf("%d", &num_id);
    
    for (int z = 0; z < itemCount; z++) {
        if (inventory[z].id == num_id) {
            if (inventory[z].isDeleted) {
                printf("Item with ID %d is already removed.\n", num_id);
                return;
            }
            inventory[z].isDeleted = 1;
            printf("Item with ID %d has been removed.\n", num_id);
            return;
        }
    }
    printf("Item with ID %d not found in inventory.\n", num_id);
}

int revenue_Check(int arr[]) {
     if (itemCount == 0) {
        printf("No sales have been made yet.\n");
        return -1;
    }
    
    int max = INT_MIN;
    int rev_id = -1;
    for (int i = 0; i < MAX_ITEMS; i++) {
        if (arr[i] < 0) arr[i] = 0;
        if (arr[i] > max) {
            max = arr[i];
            rev_id = i + 1;
        }
    }
    if (rev_id != -1) {
        printf("Item ID %d generated the most revenue of $%d\n", rev_id, max);
    }
    return rev_id;
}

void sellItem(int id, int quantitySold) {
    for (int i = 0; i < itemCount; i++) {
        if (inventory[i].id == id) {
            if (inventory[i].quantity >= quantitySold) {
                inventory[i].quantity -= quantitySold;
                inventory[i].soldCount += quantitySold;
                Income[i] += (inventory[i].price * quantitySold);
                
                printf("Sale successful! %d units of '%s' sold.\n", quantitySold, inventory[i].name);
                printf("Updated Quantity: %d, Total Sold: %d\n", inventory[i].quantity, inventory[i].soldCount);
            }
            else {
                printf("Insufficient stock for item '%s'. Available quantity: %d.\n", inventory[i].name, inventory[i].quantity);
            }
            return;
        }
    }
    printf("Item with ID %d not found in inventory.\n", id);
}

void restock(void) {
    int restock_id, rquantity;

    printf("Enter the ID of the item you want to restock: ");
    scanf("%d", &restock_id);
    printf("Enter the quantity you want to add: ");
    scanf("%d", &rquantity);

    for (int k = 0; k < itemCount; k++) {
        if (inventory[k].id == restock_id) {
            inventory[k].quantity += rquantity;
            printf("Item with ID %d restocked. New Quantity: %d\n", restock_id, inventory[k].quantity);
            return;
        }
    }

    printf("Item with ID %d not found in inventory.\n", restock_id);
}

void displayInventory(void) {
    if (itemCount == 0) {
        printf("Inventory is empty.\n");
    } else {
        printf("Item List:\n");
        for (int i = 0; i < itemCount; i++) {
            if (!inventory[i].isDeleted) {
                printf("ID: %d, Name: %s, Quantity: %d, Price: %.2f\n", 
                       inventory[i].id, inventory[i].name, inventory[i].quantity, inventory[i].price);
            }
        }
    }
}

int main() {
    int choice, id, quantitySold;
    char name[50];
    float price;

    if (!login()) {
        return 0;
    }

    loadInventoryFromFile(); // Load previous data

    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter Item ID: ");
                scanf("%d", &id);
                printf("Enter Item Name: ");
                scanf("%s", name);
                printf("Enter Item Quantity: ");
                scanf("%d", &quantitySold);
                printf("Enter Item Price: ");
                scanf("%f", &price);
                addItem(id, name, quantitySold, price);
                break;
            case 2:
                printf("Enter Item ID to Sell: ");
                scanf("%d", &id);
                printf("Enter Quantity to Sell: ");
                scanf("%d", &quantitySold);
                sellItem(id, quantitySold);
                break;
            case 3:
                displayInventory();
                break;
            case 4:
                restock();
                break;
            case 5:
                revenue_Check(Income);
                break;
            case 6:
                RemoveItem();
                break;
            case 7:
            {
                printf("Enter ID to Search Item: ");
                scanf("%d", &id);
                Item* foundItem = searchItemByID(id);
                    if (foundItem) {
                        printf("\n--- Item Found ---\n");
                        printf("ID: %d\n", foundItem->id);
                        printf("Name: %s\n", foundItem->name);
                        printf("Quantity: %d\n", foundItem->quantity);
                        printf("Price: %.2f\n", foundItem->price);
                        printf("Sold: %d\n", foundItem->soldCount);
                    }
                    else
                    {
                        printf("Item with ID %d not found in inventory.\n", id);
                    }
                    break;
            }
            case 8:
                trackSoldItems();
                break;
            case 9:
                saveInventoryToFile();
                break;
            case 10:
                printf("Exiting the system.\n");
                saveInventoryToFile(); // Save inventory before exit
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}