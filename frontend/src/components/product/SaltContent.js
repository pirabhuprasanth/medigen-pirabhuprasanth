import React from 'react';

const SaltContent = ({ salts }) => {
  if (!salts || salts.length === 0) {
    return null;
  }

  return (
    <section className="card salt-content">
      <h2>Salt Content</h2>
      <div className="salt-list">
        {salts.map((salt, index) => (
          <div key={index} className="salt-item">
            <h3>{salt.name}</h3>
            <p className="strength">{salt.strength}</p>
            <p className="description">{salt.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default SaltContent;