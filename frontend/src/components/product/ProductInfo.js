import React, { useState } from 'react';
import tabletImage from '../../assets/tablet_image.svg';

const ProductInfo = ({ details }) => {
  const [quantity, setQuantity] = useState(1);
  const [selectedStrip, setSelectedStrip] = useState('15 tablets');

  const increaseQuantity = () => setQuantity(prev => prev + 1);
  const decreaseQuantity = () => setQuantity(prev => prev > 1 ? prev - 1 : 1);

  return (
    <>
      <section className="product-info">
        <div className="product-header">
          <div className="product-image-container">
            <img src={tabletImage} alt={details.name} className="product-image" />
            <div className="discount-badge">15% OFF</div>
          </div>
          
          <div className="product-details">
            <h1>{details.name}</h1>
            <p className="manufacturer">By {details.manufacturer}</p>
            <p className="product-description">{details.description_general}</p>
            
            <div className="product-badges">
              <span className="badge badge-prescription">Prescription Required</span>
              <span className="badge badge-verified">Verified Product</span>
              <span className="badge badge-fast-delivery">Fast Delivery</span>
            </div>
          </div>
          
          <div className="product-pricing">
            <div className="price-section">
              <span className="current-price">₹34</span>
              <span className="original-price">₹40</span>
              <div className="discount-percent">15% OFF</div>
            </div>
            
            <div className="quantity-selector">
              <button className="quantity-btn" onClick={decreaseQuantity}>−</button>
              <span className="quantity-display">{quantity}</span>
              <button className="quantity-btn" onClick={increaseQuantity}>+</button>
            </div>
            
            <div className="action-buttons">
              <button className="btn-primary">Add to Cart</button>
              <button className="btn-secondary">♡</button>
            </div>
          </div>
        </div>
      </section>

      <div className="info-section">
        <h3>Uses of {details.name}</h3>
        <ul>
          {details.uses.map((use, index) => (
            <li key={index}>{use}</li>
          ))}
        </ul>
      </div>
      
      <div className="info-section">
        <h3>How {details.name} Works</h3>
        <p>{details.how_it_works}</p>
      </div>
      
      <div className="info-section">
        <h3>Side Effects of {details.name}</h3>
        <ul>
          {details.side_effects.map((effect, index) => (
            <li key={index}>{effect}</li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default ProductInfo;