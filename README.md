# ML Model Deployment API

A Flask-based API that serves two machine learning models: Iris Classification and House Price Prediction.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker
- Git

### Installation & Setup

1. Clone the repository and navigate to the project directory
2. Install Python dependencies:
   ```bash
   cd app
   pip install -r requirements.txt
   cd ..
   ```
3. Train the models:
   ```bash
   python train.py        # Creates model.pkl for Iris classification
   python train_2.py      # Creates house_price_model.pkl for house price prediction
   ```
4. Build and run the Docker container:
   ```bash
   docker build -t ml-model .
   docker run -p 9000:9000 ml-model
   ```

## 📡 API Endpoints

### Health Check
- **GET** `/health`
- Returns API status
- Example response: `{"status": "OK!"}`

### Iris Classification
- **POST** `/predict`
- Input: 4 features (sepal length, sepal width, petal length, petal width)
- Example request body:

```json
{
  "features": [
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 3.4, 5.4, 2.3]
  ]
}
```
- Output: Predicted class (0: Setosa, 1: Versicolor, 2: Virginica) and confidence score
- Example response:

```json
{
  "predictions": [
    {
      "prediction": 0,
      "confidence": 0.97
    },
    {
      "prediction": 2,
      "confidence": 0.95
    }
  ]
}
```

### House Price Prediction
- **POST** `/predict_house`
- Input: 12 house features (see Features section below)
- Example request body:

```json
{
  "features": [
    9960,
    3,
    2,
    2,
    "yes",
    "no",
    "yes",
    "no",
    "no",
    2,
    "yes",
    "semi-furnished"
  ]
}
```
- Output: Predicted house price in USD
- Example response:
```json
{
  "predicted_price": 1234567.89
}
```

## Example Usage

### Iris Classification

```bash
curl -X POST http://127.0.0.1:9000/predict \
     -H "Content-Type: application/json" \
     -d '{
       "features": [5.1, 3.5, 1.4, 0.2]
     }'
```

### House Price Prediction

```bash
curl -X POST http://127.0.0.1:9000/predict_house \
     -H "Content-Type: application/json" \
     -d '{
       "features": [
         9960, 3, 2, 2, "yes", "no", "yes", "no", "no", 2, "yes", "semi-furnished"
       ]
     }'
```

## 📋 Features

### House Price Prediction Features
1. Area (square feet)
2. Number of bedrooms
3. Number of bathrooms
4. Number of stories
5. Main road access (yes/no)
6. Guest room (yes/no)
7. Basement (yes/no)
8. Hot water heating (yes/no)
9. Air conditioning (yes/no)
10. Parking spaces
11. Preferred area (yes/no)
12. Furnishing status (furnished/semi-furnished/unfurnished)

## ⚠️ Error Handling

The API returns appropriate error messages with HTTP status codes:
- 400: Invalid input format
- 500: Server-side errors

Example error response:
```json
{
  "error": "Invalid Input: Features must be a list"
}
```

## 🔧 Technical Details

- Built with Flask
- Uses XGBoost for house price prediction
- Containerized with Docker
- Runs on port 9000

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.



