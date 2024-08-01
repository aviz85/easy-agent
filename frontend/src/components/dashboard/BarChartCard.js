import React, { useState } from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

const ChartContainer = styled(Card)`
  height: 300px;
  padding: 1rem;
`;

const BarChart = styled.div`
  display: flex;
  align-items: flex-end;
  height: 200px;
  padding-top: 20px;
`;

const Bar = styled.div`
  flex: 1;
  background-color: ${props => props.theme.colors.primary};
  margin: 0 2px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  color: white;
  font-size: 12px;
  transition: height ${props => props.theme.transitions.default}, 
              background-color ${props => props.theme.transitions.default};

  &:hover {
    background-color: ${props => props.theme.colors.primaryDark};
  }
`;

const Tooltip = styled.div`
  position: absolute;
  background-color: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.text};
  padding: 0.5rem;
  border-radius: 4px;
  box-shadow: ${props => props.theme.shadows.small};
  z-index: 10;
  opacity: 0;
  transition: opacity ${props => props.theme.transitions.default};

  &.visible {
    opacity: 1;
  }
`;

const BarChartCard = ({ data }) => {
  const [activeTooltip, setActiveTooltip] = useState(null);
  const maxValue = Math.max(...data.map(item => item.amount));

  return (
    <ChartContainer>
      <h2>Monthly Commissions</h2>
      <BarChart>
        {data.map((item, index) => (
          <Bar 
            key={item.name} 
            style={{ height: `${(item.amount / maxValue) * 100}%` }}
            onMouseEnter={() => setActiveTooltip(index)}
            onMouseLeave={() => setActiveTooltip(null)}
          >
            <span>${item.amount}</span>
            <span>{item.name}</span>
            <Tooltip className={activeTooltip === index ? 'visible' : ''}>
              {item.name}: ${item.amount}
            </Tooltip>
          </Bar>
        ))}
      </BarChart>
    </ChartContainer>
  );
};

export default BarChartCard;