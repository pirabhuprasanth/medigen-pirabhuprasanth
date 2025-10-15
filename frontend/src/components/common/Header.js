import React, { useState } from 'react';

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [cartCount, setCartCount] = useState(3);

  return (
    <>
      <header className="header">
        <div className="container">
          <a href="/" className="logo">MediCare</a>
          
          <div className="search-bar">
            <input 
              type="text" 
              className="search-input"
              placeholder="Search for medicines, health products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <div className="header-actions">
            <button className="user-icon" title="My Account">
              👤
            </button>
            <button className="cart-icon" title="Cart">
              🛒
              {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
            </button>
          </div>
        </div>
      </header>
      
      <nav className="breadcrumb">
        <div className="container">
          <ul className="breadcrumb-list">
            <li className="breadcrumb-item"><a href="/">Home</a></li>
            <li className="breadcrumb-item"><a href="/medicines">Medicines</a></li>
            <li className="breadcrumb-item"><a href="/prescription">Prescription Drugs</a></li>
            <li className="breadcrumb-item">UDILIV 300MG TABLET 15'S</li>
          </ul>
        </div>
      </nav>
    </>
  );
};

export default Header;