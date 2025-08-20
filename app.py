from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS for mobile and web clients
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8000", "http://127.0.0.1:8000", 
                   "https://yourdomain.com", "http://0.0.0.0:8000",
                   "http://192.168.*.*:*", "http://10.*.*.*:*"],  # Allow local network IPs for mobile testing
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Your WhatsApp number (with country code but without + or 00)
WHATSAPP_NUMBER = "2347026972403"

@app.route("/get_whatsapp", methods=["GET"])
def get_whatsapp():
    """Return the WhatsApp number for order processing"""
    try:
        logger.info("Received request for WhatsApp number")
        return jsonify({
            "whatsapp": WHATSAPP_NUMBER,
            "status": "success",
            "message": "WhatsApp number retrieved successfully"
        })
    except Exception as e:
        logger.error(f"Error in get_whatsapp: {str(e)}")
        return jsonify({
            "whatsapp": WHATSAPP_NUMBER,  # Fallback to ensure frontend works
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/submit_order", methods=["POST"])
def submit_order():
    """Alternative endpoint to handle order submission"""
    try:
        # Get order data from request
        order_data = request.get_json()
        
        if not order_data:
            return jsonify({
                "status": "error",
                "message": "No order data provided"
            }), 400
        
        # Extract order details
        name = order_data.get("name", "")
        phone = order_data.get("phone", "")
        address = order_data.get("address", "")
        cart_items = order_data.get("cart", [])
        
        # Validate required fields
        if not name or not phone or not address:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: name, phone, or address"
            }), 400
        
        # Format cart details
        cart_details = "\n".join([f"- {item.get('title', 'Unknown')} (${item.get('price', 0)})" 
                                 for item in cart_items])
        
        # Create the WhatsApp message
        message = f"Hello, my name is {name}.\nMy phone is {phone}.\nMy address is: {address}.\n\nI want to order:\n{cart_details}"
        
        # URL encode the message (frontend will handle this, but we provide it as an option)
        encoded_message = message.replace("\n", "%0A").replace(" ", "%20")
        
        # Create the WhatsApp URL
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
        
        logger.info(f"Order received from {name} ({phone})")
        
        return jsonify({
            "status": "success",
            "message": "Order processed successfully",
            "whatsapp_url": whatsapp_url,
            "whatsapp_number": WHATSAPP_NUMBER
        })
        
    except Exception as e:
        logger.error(f"Error in submit_order: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Order API",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run the application
    # Use host='0.0.0.0' to make it accessible on your local network
    app.run(host='0.0.0.0', port=port, debug=True)