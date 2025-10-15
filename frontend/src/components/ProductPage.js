// src/components/ProductPage.js
import React, { useState, useEffect } from 'react';
import { getProductData } from '../services/api';
import Header from './common/Header';
import Footer from './common/Footer';
import ProductInfo from './product/ProductInfo';
import SaltContent from './product/SaltContent';
import Substitutes from './product/Substitutes';
import Faqs from './product/Faqs';
import Reviews from './product/Reviews';
import './ProductPage.css';

const ProductPage = ({ token }) => {
  // Main state for all page data
  const [pageData, setPageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetching data for product with ID 1 as an example
        const data = await getProductData(1, token);
        setPageData(data);
      } catch (err) {
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [token]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="page-container">
      <Header />
      <div className="content-wrapper">
        <main className="main-content">
          {pageData && (
            <>
              <ProductInfo details={pageData.product_details} />
              <SaltContent salts={pageData.salt_content} />
              <Faqs items={pageData.faqs} saltName={pageData.salt_content[0]?.name} />
              <Reviews items={pageData.reviews} />
            </>
          )}
        </main>
        <aside className="sidebar">
          {pageData && (
            <Substitutes items={pageData.substitutes} />
          )}
        </aside>
      </div>
      <Footer />
    </div>
  );
};

export default ProductPage;