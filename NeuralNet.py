from Matrix import Matrix
import csv


class NeuralNet:
    def __init__(self, inputs=0, hidden=0, outputs=0):
        self.input_nodes = inputs
        self.hiden_nodes = hidden
        self.output_nodes = outputs

        # self.hiden_input_weights = Matrix(self.hiden_nodes, self.input_nodes)
        self.hiden_input_weights = Matrix(self.input_nodes+1, self.hiden_nodes)
        self.hiden_hiden_weights = Matrix(self.hiden_nodes+1, self.hiden_nodes)
        self.output_hiden_weights = Matrix(self.hiden_nodes+1, self.output_nodes)

        self.hiden_input_weights.randomize()
        self.hiden_hiden_weights.randomize()
        self.output_hiden_weights.randomize()

    def mutate(self, mutation_rate):
        self.hiden_input_weights.mutate(mutation_rate)
        self.hiden_hiden_weights.mutate(mutation_rate)
        self.output_hiden_weights.mutate(mutation_rate)

    def output(self, input_array):
        inputs = self.hiden_input_weights.single_column_matrix_from_array(input_array)

        input_bias = inputs.add_bias()

        hidden_inputs = self.hiden_input_weights * input_bias
        hidden_outputs = hidden_inputs.activate()
        hidden_outputs_bias = hidden_outputs.add_bias()

        hidden_inputs2 = self.hiden_hiden_weights * hidden_outputs_bias
        hidden_outputs2 = hidden_inputs2.activate()
        hidden_outputs2_bias = hidden_outputs2.add_bias()

        output_inputs = self.output_hiden_weights * hidden_outputs2_bias

        outputs = output_inputs.activate()

        return outputs.toArray()

    def crossover(self, partner):
        child = NeuralNet(self.input_nodes, self.hiden_nodes, self.output_nodes)

        child.output_hiden_weights = self.hiden_input_weights.crossover(partner.hiden_input_weights)
        child.hiden_input_weights = self.hiden_hiden_weights.crossover(partner.hiden_hiden_weights)
        child.output_hiden_weights = self.output_hiden_weights.crossover(partner.output_hiden_weights)

        return child

    def copy(self):
        new_net = NeuralNet(self.input_nodes, self.hiden_nodes, self.output_nodes)

        new_net.hiden_input_weights = self.hiden_input_weights
        new_net.hiden_hiden_weights = self.hiden_hiden_weights
        new_net.output_hiden_weights = self.output_hiden_weights

        return new_net

    def net_to_table(self):
        hiden_input_arr = self.hiden_input_weights.toArray()
        hiden_hiden_arr = self.hiden_hiden_weights.toArray()
        output_hiden_arr = self.output_hiden_weights.toArray()
        table = [hiden_input_arr, hiden_hiden_arr, output_hiden_arr]
        with open("data.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerows(table)
        return table

    def table_to_net(self):
        table = []
        with open('data.csv') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
            for r in reader:
                table.append(r)
        hiden_input_arr, hiden_hiden_arr, output_hiden_arr = table
        self.hiden_input_weights.fromArray(hiden_input_arr)
        self.hiden_hiden_weights.fromArray(hiden_hiden_arr)
        self.output_hiden_weights.fromArray(output_hiden_arr)


if __name__ == "__main__":
    neural = NeuralNet(5, 2, 4)
    print(neural.output([1, 0.5, 0.3333333, 0.125, 0.333]))
