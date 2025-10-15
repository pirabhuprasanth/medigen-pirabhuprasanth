import React from 'react';

const Substitutes = ({ items }) => {
  if (!items || items.length === 0) {
    return (
      <div className="sidebar">
        <section className="alternatives-section">
          <h2>Alternative Products</h2>
          <p className="no-substitutes">No alternatives available.</p>
        </section>
      </div>
    );
  }

  return (
    <div className="sidebar">
      <section className="alternatives-section">
        <h2>Alternative Products</h2>
        <div className="substitutes-list">
          {items.map((substitute, index) => (
            <div key={index} className="substitute-card">
              <div className="substitute-header">
                <div className="substitute-name">{substitute.name}</div>
                <div className="substitute-price">₹{substitute.price}</div>
              </div>
              <div className="substitute-manufacturer">{substitute.manufacturer}</div>
              <div className="substitute-strength">{substitute.strength}</div>
              <button className="add-btn">+ Add to Cart</button>
            </div>
          ))}
        </div>
      </section>

      <section className="quick-actions">
        <h3>Quick Actions</h3>
        <button className="quick-action-btn">
          📋 Upload Prescription
        </button>
        <button className="quick-action-btn">
          💬 Ask Pharmacist
        </button>
        <button className="quick-action-btn">
          📞 Call for Help
        </button>
        <button className="quick-action-btn">
          🚚 Track Order
        </button>
      </section>
    </div>
  );
};

export default Substitutes;