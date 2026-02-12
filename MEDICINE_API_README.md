# Medicine CRUD API Documentation

## Overview
A comprehensive CRUD API for managing medicines in the Ayurallopathy Medicine Library application. This API is built with Spring Boot and provides endpoints for creating, reading, updating, and deleting medicine records, along with advanced filtering and search capabilities.

## Base URL
```
http://localhost:8082/api/medicines
```

## Data Model

### Medicine Entity
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Long | Auto-generated | Unique identifier |
| name | String | Yes | Medicine name |
| brand | String | No | Brand or manufacturer |
| category | Enum | Yes | Ayurvedic, Allopathic, Homeopathic, or Other |
| quantity | Integer | Yes | Stock quantity |
| unit | String | No | Unit of measurement (e.g., Tablets, ml) |
| expiryDate | LocalDate | Yes | Expiration date |
| manufactureDate | LocalDate | No | Manufacturing date |
| description | String | No | Medicine description or uses |
| dosageInstructions | String | No | Recommended dosage |
| ingredients | List<String> | No | List of ingredients |
| sideEffects | List<String> | No | Known side effects |
| benefits | List<String> | No | Health benefits |
| location | String | No | Storage location |
| createdAt | Instant | Auto-generated | Creation timestamp |
| lastUpdated | Instant | Auto-generated | Last update timestamp |

### Medicine Categories
- `AYURVEDIC` - Traditional Ayurvedic medicines
- `ALLOPATHIC` - Modern allopathic medicines
- `HOMEOPATHIC` - Homeopathic medicines
- `OTHER` - Other types of medicines

## API Endpoints

### 1. Create Medicine
**POST** `/api/medicines`

Creates a new medicine record.

**Request Body:**
```json
{
  "name": "Ashwagandha Tablets",
  "brand": "Himalaya",
  "category": "AYURVEDIC",
  "quantity": 100,
  "unit": "Tablets",
  "expiryDate": "2025-12-31",
  "manufactureDate": "2024-01-15",
  "description": "Helps reduce stress and anxiety",
  "dosageInstructions": "Take 1 tablet twice daily after meals",
  "ingredients": ["Ashwagandha Extract", "Cellulose"],
  "sideEffects": ["May cause drowsiness"],
  "benefits": ["Reduces stress", "Improves energy", "Enhances immunity"],
  "location": "Shelf A1"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Ashwagandha Tablets",
  "brand": "Himalaya",
  "category": "AYURVEDIC",
  "quantity": 100,
  "unit": "Tablets",
  "expiryDate": "2025-12-31",
  "manufactureDate": "2024-01-15",
  "description": "Helps reduce stress and anxiety",
  "dosageInstructions": "Take 1 tablet twice daily after meals",
  "ingredients": ["Ashwagandha Extract", "Cellulose"],
  "sideEffects": ["May cause drowsiness"],
  "benefits": ["Reduces stress", "Improves energy", "Enhances immunity"],
  "location": "Shelf A1",
  "createdAt": "2026-02-12T10:30:00Z",
  "lastUpdated": "2026-02-12T10:30:00Z"
}
```

---

### 2. Get All Medicines
**GET** `/api/medicines`

Retrieves all medicine records.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Ashwagandha Tablets",
    "brand": "Himalaya",
    // ... other fields
  },
  {
    "id": 2,
    "name": "Paracetamol",
    "brand": "Generic",
    // ... other fields
  }
]
```

---

### 3. Get Medicine by ID
**GET** `/api/medicines/{id}`

Retrieves a specific medicine by its ID.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Ashwagandha Tablets",
  // ... all fields
}
```

**Error Response:** `404 Not Found`
```json
"Medicine not found with id: 1"
```

---

### 4. Get Medicines by Category
**GET** `/api/medicines/category/{category}`

Retrieves all medicines of a specific category.

**Parameters:**
- `category` (path) - One of: AYURVEDIC, ALLOPATHIC, HOMEOPATHIC, OTHER

**Example:**
```
GET /api/medicines/category/AYURVEDIC
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Ashwagandha Tablets",
    "category": "AYURVEDIC",
    // ... other fields
  }
]
```

---

### 5. Search Medicines by Name
**GET** `/api/medicines/search?name={searchTerm}`

Searches for medicines by name (case-insensitive, partial match).

**Query Parameters:**
- `name` (required) - Search term

**Example:**
```
GET /api/medicines/search?name=ashwa
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Ashwagandha Tablets",
    // ... other fields
  }
]
```

---

### 6. Get Expiring Soon
**GET** `/api/medicines/expiring-soon?days={days}`

Retrieves medicines expiring within the specified number of days.

**Query Parameters:**
- `days` (optional, default: 30) - Number of days

**Example:**
```
GET /api/medicines/expiring-soon?days=60
```

**Response:** `200 OK`
```json
[
  {
    "id": 3,
    "name": "Vitamin C",
    "expiryDate": "2026-03-15",
    // ... other fields
  }
]
```

---

### 7. Get Expired Medicines
**GET** `/api/medicines/expired`

Retrieves all expired medicines.

**Response:** `200 OK`
```json
[
  {
    "id": 5,
    "name": "Old Medicine",
    "expiryDate": "2025-01-15",
    // ... other fields
  }
]
```

---

### 8. Get Low Stock Medicines
**GET** `/api/medicines/low-stock?threshold={threshold}`

Retrieves medicines with quantity below or equal to the threshold.

**Query Parameters:**
- `threshold` (optional, default: 10) - Minimum quantity threshold

**Example:**
```
GET /api/medicines/low-stock?threshold=20
```

**Response:** `200 OK`
```json
[
  {
    "id": 7,
    "name": "Emergency Medicine",
    "quantity": 5,
    // ... other fields
  }
]
```

---

### 9. Update Medicine
**PUT** `/api/medicines/{id}`

Updates an existing medicine record. All fields are optional.

**Request Body:**
```json
{
  "quantity": 150,
  "location": "Shelf B2",
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Ashwagandha Tablets",
  "quantity": 150,
  "location": "Shelf B2",
  "description": "Updated description",
  "lastUpdated": "2026-02-12T14:30:00Z",
  // ... other fields
}
```

**Error Response:** `404 Not Found`
```json
"Medicine not found with id: 1"
```

---

### 10. Delete Medicine
**DELETE** `/api/medicines/{id}`

Deletes a medicine record.

**Response:** `204 No Content`

**Error Response:** `404 Not Found`
```json
"Medicine not found with id: 1"
```

---

## Error Handling

### HTTP Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `404 Not Found` - Resource not found
- `400 Bad Request` - Invalid request data

### Error Response Format
```json
"Error message describing what went wrong"
```

---

## Database Schema

The API automatically creates the following tables in PostgreSQL:

### medicines
Main table storing medicine information.

### medicine_ingredients
Junction table for storing medicine ingredients (one-to-many).

### medicine_side_effects
Junction table for storing side effects (one-to-many).

### medicine_benefits
Junction table for storing benefits (one-to-many).

---

## Setup and Configuration

### Prerequisites
- Java 17 or higher
- PostgreSQL database
- Maven

### Database Configuration
Configure in `application.properties`:
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/demoappdb
spring.datasource.username=demoappuser
spring.datasource.password=demoapp123
spring.jpa.hibernate.ddl-auto=update
```

### Running the Application
```bash
cd /var/www/spring-apps/asknehrubackend
./mvnw spring-boot:run
```

The API will be available at `http://localhost:8082`

---

## Frontend Integration

### Example: Fetch All Medicines
```typescript
const response = await fetch('http://localhost:8082/api/medicines');
const medicines = await response.json();
```

### Example: Create Medicine
```typescript
const newMedicine = {
  name: "Medicine Name",
  category: "AYURVEDIC",
  quantity: 50,
  expiryDate: "2025-12-31"
};

const response = await fetch('http://localhost:8082/api/medicines', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(newMedicine)
});

const created = await response.json();
```

### Example: Update Medicine
```typescript
const updates = {
  quantity: 75,
  location: "Shelf C3"
};

const response = await fetch(`http://localhost:8082/api/medicines/${id}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(updates)
});

const updated = await response.json();
```

### Example: Delete Medicine
```typescript
await fetch(`http://localhost:8082/api/medicines/${id}`, {
  method: 'DELETE'
});
```

---

## Testing with cURL

### Create Medicine
```bash
curl -X POST http://localhost:8082/api/medicines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Medicine",
    "category": "AYURVEDIC",
    "quantity": 100,
    "unit": "Tablets",
    "expiryDate": "2025-12-31"
  }'
```

### Get All Medicines
```bash
curl http://localhost:8082/api/medicines
```

### Get Medicine by ID
```bash
curl http://localhost:8082/api/medicines/1
```

### Update Medicine
```bash
curl -X PUT http://localhost:8082/api/medicines/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 150
  }'
```

### Delete Medicine
```bash
curl -X DELETE http://localhost:8082/api/medicines/1
```

---

## Advanced Features

### 1. Inventory Management
- Track medicine quantities
- Monitor low stock levels
- Set custom thresholds for alerts

### 2. Expiry Tracking
- Identify medicines expiring soon
- List already expired medicines
- Configure custom expiry alert periods

### 3. Categorization
- Filter by medicine type (Ayurvedic, Allopathic, etc.)
- Organize inventory by category
- Generate category-specific reports

### 4. Search and Filter
- Search by medicine name
- Filter by multiple criteria
- Case-insensitive partial matching

---

## Security Considerations

The API currently uses CORS with `origins = "*"` for development. For production:

1. Configure specific allowed origins in `MedicineController`:
   ```java
   @CrossOrigin(origins = "https://yourdomain.com")
   ```

2. Consider implementing authentication/authorization using the existing JWT configuration

3. Add validation for sensitive operations

---

## Future Enhancements

Potential improvements for the API:
- Pagination for large datasets
- Sorting options for list endpoints
- Batch operations (create, update, delete multiple)
- Medicine image upload support
- Stock history tracking
- Automatic reorder notifications
- Barcode/QR code integration
- Export to CSV/PDF
- Advanced analytics dashboard

---

## Support

For issues or questions:
- Check the logs at `/var/www/spring-apps/asknehrubackend/logs`
- Review the Spring Boot application logs
- Verify database connectivity

---

## License

This API is part of the AskNehru Backend project.
