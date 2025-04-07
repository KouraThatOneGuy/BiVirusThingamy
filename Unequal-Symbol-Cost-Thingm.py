from collections import defaultdict
import heapq

class SymbolNode:
    def __init__(self, symbol=None, cost=None):
        self.symbol = symbol
        self.cost = cost
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.cost < other.cost

class PrefixFreeCodeGenerator:
    def __init__(self, costs):
        """
        Initialize the generator with symbol costs
        
        Args:
            costs: List[int] of symbol costs where len(costs) = n
        """
        self.costs = costs
        self.n = len(costs)
        
    def generate_encoding_table(self):
        """Generate optimal prefix-free encoding table"""
        # Create initial nodes
        nodes = []
        for i, cost in enumerate(self.costs):
            node = SymbolNode(symbol=i, cost=cost)
            heapq.heappush(nodes, node)
            
        # Build tree using dynamic programming approach
        while len(nodes) > 1:
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)
            
            # Create internal node
            parent = SymbolNode(cost=left.cost + right.cost)
            parent.left = left
            parent.right = right
            
            heapq.heappush(nodes, parent)
        
        root = nodes[0]
        encoding_table = {}
        
        def build_codes(node, code=""):
            if node.symbol is not None:
                encoding_table[node.symbol] = code
                return
                
            build_codes(node.left, code + "0")
            build_codes(node.right, code + "1")
            
        build_codes(root)
        return encoding_table
    
    def encode_message(self, symbols):
        """Encode a message using the generated encoding table"""
        encoding_table = self.generate_encoding_table()
        encoded_message = ""
        
        for symbol in symbols:
            if symbol not in encoding_table:
                raise ValueError(f"Symbol {symbol} not in encoding table")
            encoded_message += encoding_table[symbol]
            
        return encoded_message
    
    def calculate_cost(self, symbols):
        """Calculate total cost of encoded message"""
        encoding_table = self.generate_encoding_table()
        total_cost = 0
        
        for symbol in symbols:
            code_length = len(encoding_table[symbol])
            total_cost += code_length * self.costs[symbol]
            
        return total_cost

# Example usage
costs = [1, 2, 3, 4]  # Costs for symbols 0, 1, 2, 3
generator = PrefixFreeCodeGenerator(costs)

# Generate encoding table
encoding_table = generator.generate_encoding_table()
print("Encoding Table:")
for symbol, code in sorted(encoding_table.items()):
    print(f"Symbol {symbol}: {code}")

# Encode a message
message = [0, 1, 2, 3]  # Message to encode
encoded_message = generator.encode_message(message)
print(f"\nEncoded message: {encoded_message}")

# Calculate total cost
total_cost = generator.calculate_cost(message)
print(f"Total cost: {total_cost}")