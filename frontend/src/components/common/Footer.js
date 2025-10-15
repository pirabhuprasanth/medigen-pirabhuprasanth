import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>MediCare</h3>
            <p>Your trusted online pharmacy for genuine medicines and healthcare products. Serving customers with quality and care since 2020.</p>
            <div className="social-links">
              <a href="#" title="Facebook">📘</a>
              <a href="#" title="Twitter">🐦</a>
              <a href="#" title="Instagram">📷</a>
              <a href="#" title="LinkedIn">💼</a>
            </div>
          </div>
          
          <div className="footer-section">
            <h4>Shop Categories</h4>
            <ul>
              <li><a href="/prescription">Prescription Medicines</a></li>
              <li><a href="/otc">Over-the-Counter</a></li>
              <li><a href="/vitamins">Vitamins & Supplements</a></li>
              <li><a href="/healthcare">Healthcare Devices</a></li>
              <li><a href="/personal-care">Personal Care</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Customer Service</h4>
            <ul>
              <li><a href="/help">Help Center</a></li>
              <li><a href="/track-order">Track Your Order</a></li>
              <li><a href="/returns">Returns & Refunds</a></li>
              <li><a href="/shipping">Shipping Info</a></li>
              <li><a href="/contact">Contact Us</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>About MediCare</h4>
            <ul>
              <li><a href="/about">About Us</a></li>
              <li><a href="/careers">Careers</a></li>
              <li><a href="/press">Press Release</a></li>
              <li><a href="/terms">Terms & Conditions</a></li>
              <li><a href="/privacy">Privacy Policy</a></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <div className="payment-methods">
            <span>We Accept: </span>
            <span>💳 💰 🏦 📱</span>
          </div>
          <p>&copy; 2025 MediCare. All rights reserved. | License No: 20B/2025</p>
          <div className="certifications">
            <span>✅ FDA Approved</span>
            <span>🔒 SSL Secured</span>
            <span>⚕️ Licensed Pharmacy</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;