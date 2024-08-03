import { useEffect, useRef, useState } from 'react'
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
  Select,
} from '@chakra-ui/react'
import BpmnViewer from 'bpmn-js/lib/NavigatedViewer';
import axios from 'axios';
import { Link } from 'react-router-dom';

export const BPMN_JS = () => {
  const [file, setFile] = useState(null);
  const [summarizationType, setSummarizationType] = useState('RAG-LLM');
  const [query, setQuery] = useState('');
  const [LLMType, setLLMType] = useState('GPT');
  const [errorText, setErrorText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const bpmnContainerRef = useRef(null);

  useEffect(() => {
    if (result) {
      previewBPMN(result);
    }
  }, [result]);

  const generateBPMN = async () => {
    setLoading(true);
    setErrorText('');
    try {
      if (!file) {
        throw new Error('Please select a file');
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('summarizationType', summarizationType);
      formData.append('query', query);
      formData.append('LLMType', LLMType);
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/bpmn-js`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(`${import.meta.env.VITE_API_URL}/${response.data}`);
      await previewBPMN(`${import.meta.env.VITE_API_URL}/${response.data}`);
    } catch (error) {
      setErrorText(error.message);
      if (error.message === 'Request failed with status code 500') {
        setErrorText('Invalid BPMN syntax generated from the file. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  }

  const previewBPMN = async (bpmnUrl) => {
    setLoading(true);
    try {
      const response = await fetch(bpmnUrl);
      if (!response.ok) {
        throw new Error('Failed to fetch BPMN file');
      }

      bpmnContainerRef.current.innerHTML = '';
      
      const bpmnXml = await response.text();
      
      const bpmnViewer = new BpmnViewer({
        container: bpmnContainerRef.current,
      });
      await bpmnViewer.importXML(bpmnXml);
    } catch (error) {
      setErrorText(error.message);
    } finally {
      setLoading(false);
    }
  }  

  return (
    <>
      <Heading as="h1" size="xl" textAlign="center" my="4" mx="4">
        BPMN Generation
      </Heading>
      <Box p="4">Go to <Link to="/bpmn-sketch-miner">BPMN Sketch Miner</Link></Box>
      <Box borderWidth="2px" borderRadius="md" p="4" mx="4" bg="gray.50">
        <FormControl mt="2">
          <FormLabel>File</FormLabel>
          <Input type="file" borderWidth="1px" borderColor="black" size="sm" onChange={e => setFile(e.target.files?.length ? (e.target.files?.length > 0 ? e.target.files[0] : null) : null)} width="50%" />
        </FormControl>
        <FormControl mt="2">
          <FormLabel>Summarization Type</FormLabel>
          <Select borderWidth="1px" borderColor="black" placeholder='Summarization type' defaultValue={summarizationType} onChange={e => setSummarizationType(e.target.value)} width="50%" >
            <option value={"RAG-LLM"}>RAG + LLM</option>
            <option value={"LLM"}>LLM</option>
          </Select>
        </FormControl>
        <FormControl mt="2">
          <FormLabel>Query</FormLabel>
          <Textarea rows={3} borderWidth="1px" borderColor="black" size="sm" placeholder='Detailed information to be provided' onChange={e => setQuery(e.target.value)} width="50%" />
        </FormControl>
        <FormControl mt="2">
          <FormLabel>LLM Type</FormLabel>
          <Select borderWidth="1px" borderColor="black" placeholder='LLM Type' defaultValue={LLMType} onChange={e => setLLMType(e.target.value)} width="50%" >
            <option value={"GPT"}>GPT</option>
            <option value={"Gemini"}>Gemini</option>
          </Select>
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
      </Box>
      <Box
        borderWidth="2px"
        borderRadius="md"
        p="4"
        mx="4"
        mt="4"
        bg="white"
        ref={bpmnContainerRef}
        style={{ height: '500px' }}
      />
    </>
  )
}