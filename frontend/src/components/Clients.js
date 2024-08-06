import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FaPlus, FaSearch, FaEdit, FaTrash } from 'react-icons/fa';
import { getClients, createClient, deleteClient } from '../services/api';
import Input from './common/Input';
import { FieldGroup, Label } from './common/FormStyles';
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

const AddClientModal = ({ isOpen, onClose, fetchClients }) => {
  const [newClient, setNewClient] = useState({
    first_name: '',
    last_name: '',
    display_name: '',
    phone_number: '',
    email: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewClient(prevState => {
      const updatedClient = { ...prevState, [name]: value };
      if (name === 'first_name' || name === 'last_name') {
        if (!updatedClient.display_name || updatedClient.display_name === `${prevState.first_name} ${prevState.last_name}`.trim()) {
          updatedClient.display_name = `${updatedClient.first_name} ${updatedClient.last_name}`.trim();
        }
      }
      return updatedClient;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createClient(newClient);
      onClose();
      fetchClients();
    } catch (error) {
      console.error('Error creating client:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal>
      <ModalContent>
        <h2>Add New Client</h2>
        <Form onSubmit={handleSubmit}>
          <Input
            type="text"
            name="first_name"
            value={newClient.first_name}
            onChange={handleChange}
            placeholder="First Name"
            required
          />
          <Input
            type="text"
            name="last_name"
            value={newClient.last_name}
            onChange={handleChange}
            placeholder="Last Name"
            required
          />
          <Input
            type="text"
            name="display_name"
            value={newClient.display_name}
            onChange={handleChange}
            placeholder="Display Name"
            required
          />
          <Input
            type="tel"
            name="phone_number"
            value={newClient.phone_number}
            onChange={handleChange}
            placeholder="Phone Number"
          />
          <Input
            type="email"
            name="email"
            value={newClient.email}
            onChange={handleChange}
            placeholder="Email"
          />
          <Button type="submit">Add Client</Button>
          <Button type="button" onClick={onClose}>Cancel</Button>
        </Form>
      </ModalContent>
    </Modal>
  );
};

const Clients = () => {
  const [clients, setClients] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [clientToDelete, setClientToDelete] = useState(null);

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      const response = await getClients();
      setClients(response);
    } catch (error) {
      console.error('Error fetching clients:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleAddClient = () => {
    setIsModalOpen(true);
  };

  const handleDeleteClient = (client) => {
    setClientToDelete(client);
    setIsConfirmationModalOpen(true);
  };

  const confirmDeleteClient = async () => {
    try {
      await deleteClient(clientToDelete.id);
      fetchClients();
    } catch (error) {
      console.error('Error deleting client:', error);
    }
    setIsConfirmationModalOpen(false);
    setClientToDelete(null);
  };

  const filteredClients = clients.filter(client =>
    client.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (client.phone_number && client.phone_number.includes(searchTerm))
  );

  return (
    <PageContainer>
      <Title>Clients</Title>
      <ActionBar>
        <Button onClick={handleAddClient}><FaPlus /> Add Client</Button>
        <SearchInput 
          type="text" 
          placeholder="Search clients..." 
          value={searchTerm}
          onChange={handleSearch}
        />
      </ActionBar>
      <Table>
        <thead>
          <tr>
            <Th>First Name</Th>
            <Th>Last Name</Th>
            <Th>Display Name</Th>
            <Th>Email</Th>
            <Th>Phone</Th>
            <Th>Actions</Th>
          </tr>
        </thead>
        <tbody>
          {filteredClients.map(client => (
            <tr key={client.id}>
              <Td>{client.first_name}</Td>
              <Td>{client.last_name}</Td>
              <Td>{client.display_name}</Td>
              <Td>{client.email}</Td>
              <Td>{client.phone_number}</Td>
              <Td>
                <Button><FaEdit /></Button>
                <Button onClick={() => handleDeleteClient(client)}><FaTrash /></Button>
              </Td>
            </tr>
          ))}
        </tbody>
      </Table>
      <AddClientModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} fetchClients={fetchClients} />
      <ConfirmationModal
        isOpen={isConfirmationModalOpen}
        onClose={() => setIsConfirmationModalOpen(false)}
        onConfirm={confirmDeleteClient}
        title="Delete Client"
        message={`Are you sure you want to delete ${clientToDelete?.display_name}?`}
      />
    </PageContainer>
  );
};

export default Clients;