import React, { useState } from 'react';
import styled from 'styled-components';
import { FaPlus, FaSearch } from 'react-icons/fa';

const PageContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: 2rem;
`;

const ActionBar = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
`;

const Button = styled.button`
  background-color: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const SearchInput = styled.input`
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid ${props => props.theme.colors.border};
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const Th = styled.th`
  text-align: left;
  padding: 1rem;
  background-color: ${props => props.theme.colors.background};
`;

const Td = styled.td`
  padding: 1rem;
  border-top: 1px solid ${props => props.theme.colors.border};
`;

const mockTransactions = [
  { id: 1, date: '2023-05-01', description: 'Insurance Premium A', amount: 500, status: 'Completed' },
  { id: 2, date: '2023-04-28', description: 'Insurance Premium B', amount: 750, status: 'Pending' },
  { id: 3, date: '2023-04-15', description: 'Commission Payment', amount: 1000, status: 'Completed' },
];

const Transactions = () => {
  const [transactions, setTransactions] = useState(mockTransactions);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    const filtered = mockTransactions.filter(transaction => 
      transaction.description.toLowerCase().includes(e.target.value.toLowerCase())
    );
    setTransactions(filtered);
  };

  return (
    <PageContainer>
      <Title>Transactions</Title>
      <ActionBar>
        <Button><FaPlus /> Add Transaction</Button>
        <SearchInput 
          type="text" 
          placeholder="Search transactions..." 
          value={searchTerm}
          onChange={handleSearch}
        />
      </ActionBar>
      <Table>
        <thead>
          <tr>
            <Th>Date</Th>
            <Th>Description</Th>
            <Th>Amount</Th>
            <Th>Status</Th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(transaction => (
            <tr key={transaction.id}>
              <Td>{transaction.date}</Td>
              <Td>{transaction.description}</Td>
              <Td>${transaction.amount}</Td>
              <Td>{transaction.status}</Td>
            </tr>
          ))}
        </tbody>
      </Table>
    </PageContainer>
  );
};

export default Transactions;