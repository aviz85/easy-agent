import React, { useState } from 'react';
import styled from 'styled-components';
import { createAgreement } from '../services/api';
import Button from './common/Button';
import Input from './common/Input';
import Card from './common/Card';

const CreateAgreementContainer = styled.div`
  padding: ${props => props.theme.spacing.lg};
  max-width: 800px;
  margin: 0 auto;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const FieldGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-weight: 500;
  margin-bottom: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.textLight};
`;

const CommissionStructure = styled.div`
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 4px;
  padding: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.md};
`;

const SuccessMessage = styled.p`
  color: ${props => props.theme.colors.success};
  text-align: center;
  margin-top: ${props => props.theme.spacing.md};
`;

const CreateAgreement = () => {
  const [agreement, setAgreement] = useState({
    company: '',
    start_date: '',
    end_date: '',
    terms: '',
    commission_structures: [{ product: '', commission_type: '', rate: '' }],
  });
  const [successMessage, setSuccessMessage] = useState('');

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
      await createAgreement(agreement);
      setSuccessMessage('Agreement created successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      console.error('Error creating agreement:', error);
    }
  };

  return (
    <CreateAgreementContainer>
      <Title>Create Agreement</Title>
      <Card>
        <Form onSubmit={handleSubmit}>
          <FieldGroup>
            <Label htmlFor="company">Company Name</Label>
            <Input
              id="company"
              type="text"
              name="company"
              value={agreement.company}
              onChange={handleChange}
              required
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="start_date">Start Date</Label>
            <Input
              id="start_date"
              type="date"
              name="start_date"
              value={agreement.start_date}
              onChange={handleChange}
              required
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="end_date">End Date</Label>
            <Input
              id="end_date"
              type="date"
              name="end_date"
              value={agreement.end_date}
              onChange={handleChange}
              required
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="terms">Agreement Terms</Label>
            <Input
              id="terms"
              as="textarea"
              name="terms"
              value={agreement.terms}
              onChange={handleChange}
              required
            />
          </FieldGroup>
          {agreement.commission_structures.map((structure, index) => (
            <CommissionStructure key={index}>
              <FieldGroup>
                <Label htmlFor={`product-${index}`}>Product</Label>
                <Input
                  id={`product-${index}`}
                  type="text"
                  name="product"
                  value={structure.product}
                  onChange={(e) => handleCommissionStructureChange(index, e)}
                  required
                />
              </FieldGroup>
              <FieldGroup>
                <Label htmlFor={`commission_type-${index}`}>Commission Type</Label>
                <Input
                  id={`commission_type-${index}`}
                  type="text"
                  name="commission_type"
                  value={structure.commission_type}
                  onChange={(e) => handleCommissionStructureChange(index, e)}
                  required
                />
              </FieldGroup>
              <FieldGroup>
                <Label htmlFor={`rate-${index}`}>Rate</Label>
                <Input
                  id={`rate-${index}`}
                  type="number"
                  name="rate"
                  value={structure.rate}
                  onChange={(e) => handleCommissionStructureChange(index, e)}
                  required
                />
              </FieldGroup>
            </CommissionStructure>
          ))}
          <Button type="button" onClick={addCommissionStructure}>Add Commission Structure</Button>
          <Button type="submit">Create Agreement</Button>
        </Form>
        {successMessage && <SuccessMessage>{successMessage}</SuccessMessage>}
      </Card>
    </CreateAgreementContainer>
  );
};

export default CreateAgreement;