import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../services/api';
import Button from './common/Button';
import Card from './common/Card';

const DashboardContainer = styled.div`
  padding: ${props => props.theme.spacing.lg};
  max-width: 1200px;
  margin: 0 auto;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${props => props.theme.spacing.lg};
`;

const SummaryCard = styled(Card)`
  h2 {
    color: ${props => props.theme.colors.primary};
    margin-bottom: ${props => props.theme.spacing.md};
  }
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
      <Grid>
        <SummaryCard>
          <h2>Active Agreements</h2>
          <p>{agreements.length}</p>
        </SummaryCard>
        <SummaryCard>
          <h2>Recent Transactions</h2>
          <p>{transactions.length}</p>
        </SummaryCard>
      </Grid>
      <Button onClick={() => console.log('Create new agreement')} style={{ marginTop: '2rem' }}>Create New Agreement</Button>
    </DashboardContainer>
  );
};

export default Dashboard;