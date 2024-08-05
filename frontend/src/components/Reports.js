import React from 'react';
import styled from 'styled-components';

const ReportsContainer = styled.div`
  padding: 2rem;
`;

const Title = styled.h1`
  margin-bottom: 2rem;
`;

const ReportList = styled.ul`
  list-style-type: none;
  padding: 0;
`;

const ReportItem = styled.li`
  margin-bottom: 1rem;
`;

const Reports = () => {
  return (
    <ReportsContainer>
      <Title>Reports</Title>
      <ReportList>
        <ReportItem>Monthly Sales Report</ReportItem>
        <ReportItem>Client Acquisition Report</ReportItem>
        <ReportItem>Commission Summary</ReportItem>
        <ReportItem>Yearly Financial Report</ReportItem>
        <ReportItem>Transaction History</ReportItem>
      </ReportList>
    </ReportsContainer>
  );
};

export default Reports;