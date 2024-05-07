import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { BPMN_JS } from './pages/bpmn-js';
import { BPMN_Sketch_Miner } from './pages/bpmn-sketch-miner';
import { Navigate } from 'react-router-dom';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate replace to="/bpmn-js" />} />
          <Route path="/bpmn-js" element={<BPMN_JS />} />
          <Route path="/bpmn-sketch-miner" element={<BPMN_Sketch_Miner />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
