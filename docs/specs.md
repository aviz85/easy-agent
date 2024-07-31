# Final Insurance Agent Commission Management System Specification

## 1. System Overview
The Insurance Agent Commission Management System is designed to help insurance agents efficiently manage their commissions from various insurance companies and investment houses. It handles different types of insurance products, calculates commissions based on specific agreements, and provides comprehensive reporting and analysis tools.

## 2. Key Features
1. User Management
2. Agreement Management
3. Product Management
4. Transaction Recording
5. Commission Calculation and Management
6. Reporting and Analysis
7. Data Import/Export
8. Notification System
9. Meeting Summary Generation

## 3. Detailed Feature Specifications

### 3.1 User Management
- User registration and authentication
- User roles (admin, agent)
- Profile management

### 3.2 Agreement Management
- Store and manage agreements between agents and insurance companies
- Support for multiple agreement types (insurance, pension, financial products)
- Commission rate storage for different product types and categories
- Payment terms management

### 3.3 Product Management
- Categorization of products (insurance, pension, financial)
- Product types within each category
- Commission structure for each product type

### 3.4 Transaction Recording
- Manual input through web interface
- Bulk import via Excel files
- Voice note or text summary input processing
- Automatic data extraction from meeting summaries

### 3.5 Commission Calculation and Management
- Real-time calculation based on transaction details and agreements
- Support for different commission types
- Handling of special conditions and thresholds
- CRUD operations for commissions

### 3.6 Reporting and Analysis
- Monthly commission forecasts
- Actual vs. expected commission comparisons
- Performance analytics by product, company, and time period
- Export capabilities (Excel, PDF)

### 3.7 Data Import/Export
- Excel file import for agreements and transactions
- PDF parsing for company-provided commission statements
- Data export for backup and analysis purposes

### 3.8 Notification System
- Reminders for expected commission payments
- Alerts for discrepancies between expected and actual commissions
- Notifications for new agreements or changes in existing ones

### 3.9 Meeting Summary Generation
- Template-based meeting summary creation
- Automatic data extraction from summaries for transaction recording
- Integration with WhatsApp for voice note input

## 4. Technical Specification

### 4.1 Backend (Django)

#### 4.1.1 Models

1. `User`
   - Fields: username, email, password, role, etc.

2. `InsuranceCompany`
   - Fields: name, contact_info, etc.

3. `Agreement`
   - Fields: agent (FK:User), company (FK:InsuranceCompany), start_date, end_date, terms (JSON)

4. `Product`
   - Fields: name, category, type, description

5. `ProductTransactionSchema`
   - Fields: product (FK:Product), field_name, field_type, is_required

6. `CommissionType` (Enum)
   - Options: SCOPE_COMMISSION, RECURRING_COMMISSION, RETENTION_BONUS, OVERRIDE_COMMISSION, TRAIL_COMMISSION, RENEWAL_COMMISSION

7. `PaymentTerms`
   - Fields:
     - payment_type (Choices: ['DAY_OF_MONTH', 'SPECIFIC_DATE'])
     - day_of_month (IntegerField, null=True)
     - specific_date (DateField, null=True)

8. `CommissionStructure`
   - Fields: agreement (FK:Agreement), product (FK:Product), commission_type (Choices:CommissionType), rate, payment_terms (FK:PaymentTerms)

9. `Transaction`
   - Fields: agent (FK:User), client_name, product (FK:Product), date, status
   - Additional fields created dynamically based on the ProductTransactionSchema

10. `Commission`
    - Fields: transaction (FK:Transaction), commission_structure (FK:CommissionStructure), amount, expected_payment_date, status

11. `MeetingSummary`
    - Fields: agent (FK:User), date, content, processed_status

#### 4.1.2 Views

1. User Management Views
2. Agreement Management Views
3. Transaction Views (CRUD)
4. Commission Views (CRUD)
5. Reporting Views
6. Data Import/Export Views
7. Meeting Summary Views
8. Payment Terms Views

### 4.2 Frontend (React)

#### 4.2.1 Components

1. Dashboard (with CRUD tables)
2. Agreement Manager
3. Transaction Entry Form
4. Commission Calculator (interactive and automated)
5. Report Generator
6. File Upload Component
7. Meeting Summary Wizard
8. Notification Center
9. PaymentTermsManager

#### 4.2.2 Pages

1. Login/Registration Page
2. User Profile Page
3. Dashboard Page
4. Agreements Page
5. Transactions Page
6. Commissions Page
7. Reports Page
8. Settings Page
9. Meeting Summary Wizard Page
10. Payment Terms Page

### 4.3 API Endpoints

1. `/api/users/`
2. `/api/agreements/`
3. `/api/products/`
4. `/api/transactions/`
5. `/api/commissions/`
6. `/api/reports/`
7. `/api/import/`
8. `/api/export/`
9. `/api/meetings/`
10. `/api/payment-terms/`

### 4.4 External Integrations

1. WhatsApp API for voice note and message processing
2. PDF parsing library for commission statement processing
3. Excel library for file import/export

## 5. Data Flow

1. User inputs transaction data (manual, voice, text, or file upload)
2. System processes input and creates Transaction records
3. Commission Calculation engine computes expected commissions based on agreements and commission structures
4. Reporting engine generates forecasts and comparisons
5. Notification system alerts users of important events or discrepancies

## 6. Security Considerations

1. Implement robust authentication and authorization
2. Encrypt sensitive data (personal information, financial details)
3. Secure API endpoints with proper authentication
4. Implement rate limiting to prevent abuse
5. Regular security audits and updates

## 7. Scalability Considerations

1. Design database schema for efficient querying of large datasets
2. Implement caching mechanisms for frequently accessed data
3. Consider using task queues for background processing of imports and calculations
4. Design the system to be horizontally scalable

## 8. Future Enhancements

1. Mobile app development
2. AI-powered commission prediction and optimization
3. Integration with additional financial software and APIs
4. Advanced analytics and business intelligence features

## 9. Additional Implementation Considerations

### 9.1 Dynamic Transaction Fields
- Implement a system to dynamically create and manage transaction fields based on the ProductTransactionSchema.
- Ensure that the frontend can adapt to these dynamic fields when rendering forms and tables.

### 9.2 Commission Calculation Logic
- Develop a flexible calculation engine that can handle different commission structures for each product.
- Implement calculation methods for each CommissionType, ensuring that the logic correctly applies the appropriate rate and payment terms.

### 9.3 Meeting Summary Wizard
- Design a user-friendly workflow for inputting and processing meeting summaries.
- Consider making this wizard accessible from the dashboard or as a standalone page for quick access.

### 9.4 Dashboard Enhancements
- Implement CRUD functionality directly in the dashboard tables for quick edits.
- Integrate the commission calculator into the dashboard for easy access and automated calculations within reports.

### 9.5 Payment Terms Handling
- Handle edge cases in payment terms, such as months with fewer than 31 days or leap years.
- Implement logic to accurately forecast commission payments based on the defined payment terms.

### 9.6 Data Validation and Consistency
- Implement strict validation rules to ensure data consistency across the dynamic fields, commission structures, and payment terms.
- Develop a system to handle updates to product schemas and commission structures without breaking existing data.

### 9.7 User Interface Considerations
- Create intuitive interfaces for users to set and edit complex data structures like commission types and payment terms.
- Provide clear labels and potentially short descriptions for each CommissionType to help users understand the differences.

### 9.8 Reporting and Analytics
- Design reports to group and summarize commissions by CommissionType and payment terms, allowing for easy comparison and analysis.
- Develop cash flow projections based on the specified payment terms.

### 9.9 Data Migration Strategy
- If updating an existing system, create a migration plan to convert any existing data to the new structures (e.g., commission types, payment terms).
- Ensure that all related functionalities (calculations, reports, etc.) are updated to work with the new data models.