# AI-Enhanced Customer Complaint Management System

An intelligent customer complaint management system that leverages machine learning to automatically analyze and rate customer reviews and complaints using AI21 embeddings and neural networks.

## 🚀 Features

- **AI-Powered Review Analysis**: Automatically rates customer reviews from 1-5 stars using a trained neural network
- **Text Embeddings**: Utilizes AI21's embedding API for sophisticated text understanding
- **Customer Management**: Track and manage customer information
- **Product Management**: Organize complaints by product categories
- **Real-time Processing**: Flask-based REST API for real-time complaint processing
- **Interactive Frontend**: User-friendly web interface for complaint submission and tracking
- **Database Integration**: PostgreSQL database for persistent data storage

## 📁 Project Structure

```
ai-enhanced-customer-complaint-management/
├── backend/
│   ├── main.py           # Flask API server
│   ├── model.py          # AI model wrapper class
│   └── reviewsmodel.h5   # Trained Keras model
├── frontend/
│   ├── complaint.html    # Complaint submission form
│   ├── feedback.html     # Feedback interface
│   ├── products.html     # Product management
│   ├── status.html       # Status tracking
│   ├── check_customer.html # Customer lookup
│   └── style*.css        # Styling files
├── model/
│   ├── trial.ipynb       # Model training notebook
│   └── embeddings.csv    # Pre-processed embeddings data
└── README.md
```

## 🧠 Machine Learning Model

The system uses a deep neural network trained on customer review embeddings:

- **Input**: 1024-dimensional text embeddings from AI21 API
- **Architecture**: 
  - Dense layer (512 neurons, ReLU)
  - Dense layer (1024 neurons, ReLU)
  - Dense layer (2048 neurons, ReLU)
  - Dense layer (128 neurons, ReLU)
  - Output layer (5 neurons, Softmax) for 1-5 star rating classification
- **Training**: Supervised learning on customer review data


## 🔧 API Endpoints

The Flask backend provides REST API endpoints for:
- Product management
- Customer lookup
- Complaint submission
- Review rating prediction

## 🎯 Usage

1. **Submit Complaints**: Use the web interface to submit customer complaints
2. **Automatic Rating**: The AI model automatically assigns ratings to reviews
3. **Track Status**: Monitor complaint status and resolution progress
4. **Customer Management**: Look up and manage customer information
5. **Product Organization**: Categorize complaints by product type
