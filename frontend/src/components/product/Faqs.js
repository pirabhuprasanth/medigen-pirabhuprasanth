import React, { useState } from 'react';

const Faqs = ({ items, saltName }) => {
  const [openFaq, setOpenFaq] = useState(null);

  if (!items || items.length === 0) {
    return null;
  }

  const toggleFaq = (index) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <section className="card faqs">
      <h2>Frequently Asked Questions about {saltName}</h2>
      <div className="faq-list">
        {items.map((faq, index) => (
          <div key={index} className="faq-item">
            <button 
              className={`faq-question ${openFaq === index ? 'active' : ''}`}
              onClick={() => toggleFaq(index)}
            >
              {faq.question}
              <span className="faq-toggle">{openFaq === index ? '−' : '+'}</span>
            </button>
            {openFaq === index && (
              <div className="faq-answer">
                <p>{faq.answer}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
};

export default Faqs;