# 🔑 API Keys Setup Guide
## Enhanced Electrical Engineering System - Production Deployment

### 📋 **OVERVIEW**
This guide provides step-by-step instructions for obtaining and configuring API keys for all 7 supplier integrations in the Enhanced Electrical Engineering System.

**System Status:** 85% Complete - All calculators working 100%
**Current Phase:** API Key Configuration & Production Deployment
**Estimated Completion Time:** 2-3 hours for all API keys

---

## 🏢 **SUPPLIER API KEY REQUIREMENTS**

### **1. DigiKey Electronics API** ⭐ HIGH PRIORITY
**Purpose:** Electronic component search, pricing, and availability
**Website:** https://www.digikey.com/

#### Steps to Obtain DigiKey API Key:
1. **Create DigiKey Account**
   - Go to https://www.digikey.com/
   - Click "Sign Up" → "Create Account"
   - Complete business/individual registration

2. **Request API Access**
   - Login to DigiKey Developer Portal: https://developer.digikey.com/
   - Navigate to "API Keys" → "Generate New Key"
   - Complete application form:
     - Company name
     - API usage description: "Electrical engineering project management system for construction and maintenance teams"
     - Expected usage volume: "Moderate (up to 1000 requests/day)"

3. **API Key Configuration**
   ```
   Required Environment Variable: DIGIKEY_API_KEY
   Format: Base64 encoded credentials
   Rate Limits: 1000 requests/hour
   Documentation: https://developer.digikey.com/page/diode-and-discrete-products-api-v1
   ```

---

### **2. Mouser Electronics API** ⭐ HIGH PRIORITY
**Purpose:** Component search, real-time pricing, stock availability
**Website:** https://www.mouser.com/

#### Steps to Obtain Mouser API Key:
1. **Create Mouser Account**
   - Visit https://www.mouser.com/
   - Click "My Account" → "Create Account"
   - Complete registration with business information

2. **Enable API Access**
   - Navigate to Account Settings → "Developer API"
   - Click "Request API Access"
   - Provide project description: "Electrical engineering calculator integration for construction project management"

3. **API Key Details**
   ```
   Required Environment Variable: MOUSER_API_KEY
   Format: Alphanumeric string
   Rate Limits: 500 requests/hour (free tier)
   Documentation: https://www.mouser.com/api-resources/
   ```

---

### **3. UL (Underwriters Laboratories) API** 🔍 VERIFICATION PRIORITY
**Purpose:** Component safety certification and compliance verification
**Website:** https://www.ul.com/

#### Steps to Obtain UL API Access:
1. **Create UL Account**
   - Go to https://www.ul.com/
   - Register for UL Product iQ database access
   - Select "Developer" or "Business" account type

2. **API Registration**
   - Contact UL Developer Support: developers@ul.com
   - Request API access for electrical component verification
   - Provide use case: "Automated NEC compliance checking for electrical construction projects"

3. **API Key Configuration**
   ```
   Required Environment Variable: UL_API_KEY
   Type: OAuth 2.0 token
   Rate Limits: 1000 requests/day (standard)
   Documentation: Contact UL for access
   ```

---

### **4. TrustedParts API** 📦 SUPPLY CHAIN
**Purpose:** Multi-supplier price comparison and availability
**Website:** https://www.trustedparts.com/

#### Steps to Obtain TrustedParts API Key:
1. **Create TrustedParts Account**
   - Visit https://www.trustedparts.com/
   - Click "Sign Up" → "Get API Access"
   - Complete business verification

2. **API Key Generation**
   - Login to https://developer.trustedparts.com/
   - Navigate to "API Keys" → "Create New Key"
   - Select usage tier: "Developer" or "Production"

3. **API Configuration**
   ```
   Required Environment Variable: TRUSTEDPARTS_API_KEY
   Format: UUID format
   Rate Limits: 10,000 requests/month (free)
   Documentation: https://developer.trustedparts.com/docs/
   ```

---

### **5. WinSource Electronics API** 💾 INVENTORY
**Purpose:** Component inventory tracking and pricing
**Website:** https://www.winsource.com/

#### Steps to Obtain WinSource API Key:
1. **WinSource Account Setup**
   - Visit https://www.winsource.com/
   - Create business account with sales inquiry
   - Contact sales team: sales@winsource.com

2. **API Access Request**
   - Request developer API access during account setup
   - Provide project details: "Electrical engineering project management system"
   - Expected integration: Component search and pricing

3. **API Details**
   ```
   Required Environment Variable: WINSOURCE_API_KEY
   Type: Bearer token
   Rate Limits: Contact WinSource for limits
   Documentation: Provided upon approval
   ```

---

### **6. SourceEngine API** 🔧 DISTRIBUTION
**Purpose:** Global component sourcing and distribution tracking
**Website:** https://www.sourceengine.com/

#### Steps to Obtain SourceEngine API Access:
1. **SourceEngine Account Creation**
   - Visit https://www.sourceengine.com/
   - Register for business account
   - Complete supplier verification process

2. **API Integration Request**
   - Contact API support: api@sourceengine.com
   - Request REST API access for component sourcing
   - Provide integration scope: "Electrical construction project management"

3. **API Configuration**
   ```
   Required Environment Variable: SOURCENGINE_API_KEY
   Format: JWT token
   Rate Limits: Custom based on partnership
   Documentation: Available upon approval
   ```

---

### **7. Luminovo API** 🎯 PROCUREMENT
**Purpose:** Intelligent component sourcing and supply chain optimization
**Website:** https://www.luminovo.com/

#### Steps to Obtain Luminovo API Access:
1. **Luminovo Platform Account**
   - Visit https://www.luminovo.com/
   - Create enterprise account
   - Complete business verification

2. **API Partnership Request**
   - Contact partnerships team: partnerships@luminovo.com
   - Request API access for procurement optimization
   - Present use case: "Automated electrical component sourcing for construction projects"

3. **API Key Setup**
   ```
   Required Environment Variable: LUMINOVO_API_KEY
   Type: OAuth 2.0 client credentials
   Rate Limits: Enterprise tier (contact Luminovo)
   Documentation: https://docs.luminovo.com/api/
   ```

---

## 🔧 **IMPLEMENTATION STEPS**

### **Step 1: Environment File Update**
After obtaining all API keys, update your `.env` file:

```bash
# Supplier API Keys (Replace placeholders with actual keys)
DIGIKEY_API_KEY=your_actual_digikey_api_key_here
MOUSER_API_KEY=your_actual_mouser_api_key_here
UL_API_KEY=your_actual_ul_api_key_here
TRUSTEDPARTS_API_KEY=your_actual_trustedparts_api_key_here
WINSOURCE_API_KEY=your_actual_winsource_api_key_here
SOURCENGINE_API_KEY=your_actual_sourcengine_api_key_here
LUMINOVO_API_KEY=your_actual_luminovo_api_key_here

# Additional APIs
SERPER_API_KEY=your_actual_serper_api_key_here
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### **Step 2: API Integration Testing**
```bash
# Test all supplier APIs
python -c "
from supplier_integration_fixed import *
import os

# Test DigiKey API
print('Testing DigiKey API...')
digikey = DigiKeyAPI()
result = digikey.search_components('resistor 10k ohm')
print(f'DigiKey Status: {\"✓ Working\" if result else \"✗ Failed\"}')

# Test Mouser API
print('Testing Mouser API...')
mouser = MouserAPI()
result = mouser.search_components('capacitor 100uF')
print(f'Mouser Status: {\"✓ Working\" if result else \"✗ Failed\"}')

print('All supplier APIs tested!')
"
```

### **Step 3: Production Database Migration**
```bash
# Migrate from SQLite to PostgreSQL for production
python init_database_final.py --production
```

---

## 🎯 **PRIORITIZATION STRATEGY**

### **Phase 1: Essential APIs (Week 1)**
1. **DigiKey** - Highest priority, most comprehensive
2. **Mouser** - Strong competition data
3. **TrustedParts** - Price comparison engine

### **Phase 2: Verification APIs (Week 2)**
1. **UL** - Safety compliance verification
2. **WinSource** - Additional pricing data

### **Phase 3: Advanced APIs (Week 3)**
1. **SourceEngine** - Global sourcing
2. **Luminovo** - Procurement optimization

---

## 📊 **TESTING & VALIDATION**

### **API Health Check Endpoint**
The system includes `/api/health` endpoint for monitoring:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "apis": {
    "digikey": "connected",
    "mouser": "connected",
    "ul": "connected",
    "trustedparts": "connected",
    "winsource": "connected",
    "sourceengine": "connected",
    "luminovo": "connected"
  },
  "database": "connected",
  "calculators": "operational"
}
```

---

## 🛡️ **SECURITY CONSIDERATIONS**

### **API Key Security:**
- ✅ Store all keys in environment variables
- ✅ Never commit keys to version control
- ✅ Use different keys for development/production
- ✅ Implement rate limiting (already configured)
- ✅ Monitor API usage and costs

### **Best Practices:**
- Set up API usage monitoring
- Implement retry logic for failed requests
- Cache responses to reduce API calls
- Log all API interactions for debugging

---

## 📞 **SUPPORT & RESOURCES**

### **API Documentation Links:**
- DigiKey: https://developer.digikey.com/
- Mouser: https://www.mouser.com/api-resources/
- TrustedParts: https://developer.trustedparts.com/
- UL: Contact support for documentation access
- WinSource, SourceEngine, Luminovo: Contact respective support teams

### **Implementation Support:**
- **Technical Issues:** Review error logs in `/logs/` directory
- **Rate Limits:** Monitor API usage at supplier dashboards
- **Integration Testing:** Use `enhanced_demo_app.py` for validation

---

## ✅ **DEPLOYMENT CHECKLIST**

- [ ] DigiKey API key configured
- [ ] Mouser API key configured  
- [ ] UL API access approved
- [ ] TrustedParts API key configured
- [ ] WinSource API access approved
- [ ] SourceEngine API access approved
- [ ] Luminovo API partnership established
- [ ] All APIs tested and operational
- [ ] Production database configured
- [ ] Environment variables secured
- [ ] Monitoring and logging enabled
- [ ] Performance testing completed

---

**Next Steps:** After API keys are configured, proceed with production deployment and field testing with construction and maintenance engineers.

**Estimated Timeline:** 2-3 days for all API keys, 1-2 days for integration testing, 1 week for production deployment.
