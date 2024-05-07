import { useState } from 'react'
import {
  FormControl,
  FormLabel,
  Heading,
  Box,
  Button,
  Alert,
  AlertIcon,
  Input,
  Textarea,
} from '@chakra-ui/react'
import axios from 'axios';

export const BPMN_Sketch_Miner = () => {
  const [file, setFile] = useState(null);
  const [errorText, setErrorText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const generateBPMN = async () => {
    setLoading(true);
    setErrorText('');
    try {
      if (!file) {
        throw new Error('Please select a file');
      }

      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/bpmn-sketch-miner`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      setErrorText(error.message);
    } finally {
      setLoading(false);
    }
  }
  
  const copyResult = () => {
    navigator.clipboard.writeText(result);
  }

  return (
    <>
      <Heading as="h1" size="xl" textAlign="center" my="4" mx="4">
        BPMN Generation
      </Heading>
      <Box borderWidth="2px" borderRadius="md" p="4" mx="4" bg="gray.50">
        <FormControl mt="2">
          <FormLabel>File</FormLabel>
          <Input type="file" borderWidth="1px" borderColor="black" size="sm" onChange={e => setFile(e.target.files?.length ? (e.target.files?.length > 0 ? e.target.files[0] : null) : null)} width="50%" />
        </FormControl>
        <FormControl mt="2">
          <Button colorScheme="green" size="md" mx="1" isLoading={loading} onClick={generateBPMN}>Generate</Button>
          {errorText && (
            <Alert status="error" my="2" width="50%">
              <AlertIcon />
              {errorText}
            </Alert>
          )}
        </FormControl>
        <FormControl mt="2">
          <FormLabel>Result</FormLabel>
          <Textarea rows={10} borderWidth="1px" borderColor="black" size="sm" value={result} readOnly width="50%" />
        </FormControl>
        <FormControl mt="2">
          <Button colorScheme="green" size="md" mx="1" onClick={copyResult}>Copy</Button>
        </FormControl>
        <FormControl mt="2">
          <iframe src="https://www.bpmn-sketch-miner.ai/index.html" width="100%" height="800px" />
        </FormControl>
      </Box>
    </>
  )
}