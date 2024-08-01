import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../services/api';
import Button from './common/Button';

const DashboardContainer = styled.div`
  padding: 2rem;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: 1rem;
`;

const SummaryCard = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Dashboard = () => {
  const [agreements, setAgreements] = useState([]);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const agreementsResponse = await api.get('/agreements/');
        setAgreements(agreementsResponse.data);

        const transactionsResponse = await api.get('/transactions/');
        setTransactions(transactionsResponse.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <DashboardContainer>
      <Title>Dashboard</Title>
      <SummaryCard>
        <h2>Active Agreements: {agreements.length}</h2>
      </SummaryCard>
      <SummaryCard>
        <h2>Recent Transactions: {transactions.length}</h2>
      </SummaryCard>
      <Button onClick={() => console.log('Create new agreement')}>Create New Agreement</Button>
    </DashboardContainer>
  );
};

export default Dashboard;