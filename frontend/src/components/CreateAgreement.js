import React, { useState } from 'react';
import styled from 'styled-components';
import api from '../services/api';
import Button from './common/Button';
import Input from './common/Input';

const CreateAgreementContainer = styled.div`
  padding: 2rem;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: 1rem;
`;

const Form = styled.form`
  max-width: 600px;
`;

const CreateAgreement = () => {
  const [agreement, setAgreement] = useState({
    company: '',
    start_date: '',
    end_date: '',
    terms: '',
    commission_structures: [{ product: '', commission_type: '', rate: '' }],
  });

  const handleChange = (e) => {
    setAgreement({ ...agreement, [e.target.name]: e.target.value });
  };

  const handleCommissionStructureChange = (index, e) => {
    const updatedStructures = agreement.commission_structures.map((structure, i) => {
      if (i === index) {
        return { ...structure, [e.target.name]: e.target.value };
      }
      return structure;
    });
    setAgreement({ ...agreement, commission_structures: updatedStructures });
  };

  const addCommissionStructure = () => {
    setAgreement({
      ...agreement,
      commission_structures: [...agreement.commission_structures, { product: '', commission_type: '', rate: '' }],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/agreements/', agreement);
      alert('Agreement created successfully');
    } catch (error) {
      console.error('Error creating agreement:', error);
      alert('Failed to create agreement');
    }
  };

  return (
    <CreateAgreementContainer>
      <Title>Create Agreement</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          name="company"
          value={agreement.company}
          onChange={handleChange}
          placeholder="Company Name"
          required
        />
        <Input
          type="date"
          name="start_date"
          value={agreement.start_date}
          onChange={handleChange}
          required
        />
        <Input
          type="date"
          name="end_date"
          value={agreement.end_date}
          onChange={handleChange}
          required
        />
        <Input
          as="textarea"
          name="terms"
          value={agreement.terms}
          onChange={handleChange}
          placeholder="Agreement Terms"
          required
        />
        {agreement.commission_structures.map((structure, index) => (
          <div key={index}>
            <Input
              type="text"
              name="product"
              value={structure.product}
              onChange={(e) => handleCommissionStructureChange(index, e)}
              placeholder="Product"
              required
            />
            <Input
              type="text"
              name="commission_type"
              value={structure.commission_type}
              onChange={(e) => handleCommissionStructureChange(index, e)}
              placeholder="Commission Type"
              required
            />
            <Input
              type="number"
              name="rate"
              value={structure.rate}
              onChange={(e) => handleCommissionStructureChange(index, e)}
              placeholder="Rate"
              required
            />
          </div>
        ))}
        <Button type="button" onClick={addCommissionStructure}>Add Commission Structure</Button>
        <Button type="submit">Create Agreement</Button>
      </Form>
    </CreateAgreementContainer>
  );
};

export default CreateAgreement;