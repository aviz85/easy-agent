import React from 'react';
import styled from 'styled-components';
import { FaFileContract, FaUsers, FaMoneyBillWave, FaClipboardList, FaPlus, FaChartLine, FaFileAlt } from 'react-icons/fa';
import { MdNotifications } from 'react-icons/md';
import StatCard from './dashboard/StatCard';
import PieChartCard from './dashboard/PieChartCard';
import BarChartCard from './dashboard/BarChartCard';
import QuickActions from './dashboard/QuickActions';

const DashboardContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const ChartGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
  }
`;

const Dashboard = () => {
  const stats = [
    { title: 'Total Agreements', value: 24, icon: FaFileContract },
    { title: 'Active Clients', value: 156, icon: FaUsers },
    { title: 'This Month\'s Commission', value: '$5,500', icon: FaMoneyBillWave },
    { title: 'Pending Transactions', value: 7, icon: FaClipboardList },
  ];

  const productData = [
    { title: 'Life Insurance', value: 400, color: '#0088FE' },
    { title: 'Health Insurance', value: 300, color: '#00C49F' },
    { title: 'Auto Insurance', value: 300, color: '#FFBB28' },
    { title: 'Home Insurance', value: 200, color: '#FF8042' },
  ];

  const monthlyCommissions = [
    { name: 'Jan', amount: 4000 },
    { name: 'Feb', amount: 3000 },
    { name: 'Mar', amount: 5000 },
    { name: 'Apr', amount: 4500 },
    { name: 'May', amount: 6000 },
    { name: 'Jun', amount: 5500 },
  ];

  const quickActions = [
    { title: 'New Agreement', icon: FaPlus, action: () => console.log('Create new agreement') },
    { title: 'New Client', icon: FaUsers, action: () => console.log('Add new client') },
    { title: 'View Commissions', icon: FaChartLine, action: () => console.log('View commissions') },
    { title: 'Generate Report', icon: FaFileAlt, action: () => console.log('Generate report') },
  ];

  return (
    <DashboardContainer>
      <Title><MdNotifications /> Dashboard</Title>
      
      <Grid>
        {stats.map((stat, index) => (
          <StatCard 
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            onClick={() => console.log(`Clicked on ${stat.title}`)}
          />
        ))}
      </Grid>

      <ChartGrid>
        <PieChartCard data={productData} />
        <BarChartCard data={monthlyCommissions} />
      </ChartGrid>

      <QuickActions actions={quickActions} />
    </DashboardContainer>
  );
};

export default Dashboard;