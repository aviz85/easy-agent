import React, { useState } from 'react';
import styled from 'styled-components';
import { FaFileUpload, FaPlus, FaSearch } from 'react-icons/fa';

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

const mockAgreements = [
  { id: 1, name: 'Insurance Policy A', client: 'John Doe', date: '2023-05-01', status: 'Active' },
  { id: 2, name: 'Insurance Policy B', client: 'Jane Smith', date: '2023-04-15', status: 'Pending' },
  { id: 3, name: 'Insurance Policy C', client: 'Bob Johnson', date: '2023-03-22', status: 'Active' },
];

const Agreements = () => {
  const [agreements, setAgreements] = useState(mockAgreements);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    const filtered = mockAgreements.filter(agreement => 
      agreement.name.toLowerCase().includes(e.target.value.toLowerCase()) ||
      agreement.client.toLowerCase().includes(e.target.value.toLowerCase())
    );
    setAgreements(filtered);
  };

  return (
    <PageContainer>
      <Title>Agreements</Title>
      <ActionBar>
        <div>
          <Button><FaFileUpload /> Import PDF</Button>
          <Button style={{ marginLeft: '1rem' }}><FaPlus /> Add Manually</Button>
        </div>
        <SearchInput 
          type="text" 
          placeholder="Search agreements..." 
          value={searchTerm}
          onChange={handleSearch}
        />
      </ActionBar>
      <Table>
        <thead>
          <tr>
            <Th>Agreement Name</Th>
            <Th>Client</Th>
            <Th>Date</Th>
            <Th>Status</Th>
          </tr>
        </thead>
        <tbody>
          {agreements.map(agreement => (
            <tr key={agreement.id}>
              <Td>{agreement.name}</Td>
              <Td>{agreement.client}</Td>
              <Td>{agreement.date}</Td>
              <Td>{agreement.status}</Td>
            </tr>
          ))}
        </tbody>
      </Table>
    </PageContainer>
  );
};

export default Agreements;