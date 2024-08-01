import React from 'react';
import styled from 'styled-components';
import { PieChart } from 'react-minimal-pie-chart';
import Card from '../common/Card';
import { FaInfoCircle } from 'react-icons/fa';

const ChartContainer = styled(Card)`
  height: 300px;
  padding: 1rem;
  position: relative;
`;

const ChartOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity ${props => props.theme.transitions.default};

  &:hover {
    opacity: 1;
  }
`;

const PieChartCard = ({ data }) => (
  <ChartContainer>
    <h2>Product Distribution</h2>
    <PieChart
      data={data}
      label={({ dataEntry }) => `${Math.round(dataEntry.percentage)}%`}
      labelStyle={{
        fontSize: '5px',
        fontFamily: 'sans-serif',
      }}
      radius={42}
      labelPosition={112}
    />
    <ChartOverlay>
      <FaInfoCircle /> Click for detailed report
    </ChartOverlay>
  </ChartContainer>
);

export default PieChartCard;