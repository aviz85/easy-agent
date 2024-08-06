import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import { getAgreements, createAgreement, updateAgreement, deleteAgreement } from '../services/api';
import Input from './common/Input';
import Button from './common/Button';
import ConfirmationModal from './common/ConfirmationModal';

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

const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
`;

const ModalContent = styled.div`
  background-color: white;
  padding: 2rem;
  border-radius: 4px;
  width: 80%;
  max-width: 500px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const AgreementModal = ({ isOpen, onClose, agreement, onSubmit }) => {
  const [formData, setFormData] = useState(agreement || {
    company: '',
    start_date: '',
    end_date: '',
    terms: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (!isOpen) return null;

  return (
    <Modal>
      <ModalContent>
        <h2>{agreement ? 'Edit Agreement' : 'Add Agreement'}</h2>
        <Form onSubmit={handleSubmit}>
          <Input
            type="text"
            name="company"
            value={formData.company}
            onChange={handleChange}
            placeholder="Company"
            required
          />
          <Input
            type="date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            required
          />
          <Input
            type="date"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
            required
          />
          <Input
            as="textarea"
            name="terms"
            value={formData.terms}
            onChange={handleChange}
            placeholder="Agreement Terms"
            required
          />
          <Button type="submit">{agreement ? 'Update' : 'Add'} Agreement</Button>
          <Button type="button" onClick={onClose}>Cancel</Button>
        </Form>
      </ModalContent>
    </Modal>
  );
};

const AgreementManagement = () => {
  const [agreements, setAgreements] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentAgreement, setCurrentAgreement] = useState(null);
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [agreementToDelete, setAgreementToDelete] = useState(null);

  useEffect(() => {
    fetchAgreements();
  }, []);

  const fetchAgreements = async () => {
    try {
      const response = await getAgreements();
      setAgreements(response);
    } catch (error) {
      console.error('Error fetching agreements:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleAddAgreement = () => {
    setCurrentAgreement(null);
    setIsModalOpen(true);
  };

  const handleEditAgreement = (agreement) => {
    setCurrentAgreement(agreement);
    setIsModalOpen(true);
  };

  const handleDeleteAgreement = (agreement) => {
    setAgreementToDelete(agreement);
    setIsConfirmationModalOpen(true);
  };

  const handleModalSubmit = async (formData) => {
    try {
      if (currentAgreement) {
        await updateAgreement(currentAgreement.id, formData);
      } else {
        await createAgreement(formData);
      }
      setIsModalOpen(false);
      fetchAgreements();
    } catch (error) {
      console.error('Error saving agreement:', error);
    }
  };

  const confirmDeleteAgreement = async () => {
    try {
      await deleteAgreement(agreementToDelete.id);
      fetchAgreements();
    } catch (error) {
      console.error('Error deleting agreement:', error);
    }
    setIsConfirmationModalOpen(false);
    setAgreementToDelete(null);
  };

  const filteredAgreements = agreements.filter(agreement =>
    agreement.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agreement.terms.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <PageContainer>
      <Title>Agreements</Title>
      <ActionBar>
        <Button onClick={handleAddAgreement}><FaPlus /> Add Agreement</Button>
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
            <Th>Company</Th>
            <Th>Start Date</Th>
            <Th>End Date</Th>
            <Th>Actions</Th>
          </tr>
        </thead>
        <tbody>
          {filteredAgreements.map(agreement => (
            <tr key={agreement.id}>
              <Td>{agreement.company}</Td>
              <Td>{agreement.start_date}</Td>
              <Td>{agreement.end_date}</Td>
              <Td>
                <Button onClick={() => handleEditAgreement(agreement)}><FaEdit /></Button>
                <Button onClick={() => handleDeleteAgreement(agreement)}><FaTrash /></Button>
              </Td>
            </tr>
          ))}
        </tbody>
      </Table>
      <AgreementModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        agreement={currentAgreement}
        onSubmit={handleModalSubmit}
      />
      <ConfirmationModal
        isOpen={isConfirmationModalOpen}
        onClose={() => setIsConfirmationModalOpen(false)}
        onConfirm={confirmDeleteAgreement}
        title="Delete Agreement"
        message={`Are you sure you want to delete the agreement with ${agreementToDelete?.company}?`}
      />
    </PageContainer>
  );
};

export default AgreementManagement;