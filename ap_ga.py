import tkinter as tk
import numpy as np
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# このグローバル変数はGAの試行回数を制御します
#np.random.seed(0)
file_path = "" # 選択されたファイルパスを保存する変数

def create_gui():
    """GUIの主要なウィンドウとウィジェットを作成・配置する関数です。"""
    root = tk.Tk()
    root.title("GA for Knapsack Problem")
    root.geometry("900x600")

    

    # メインのコンテナフレームを作成
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # スクロールバー
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # GAパラメータ入力用のフレーム
    param_frame = ttk.LabelFrame(scrollable_frame, text="GA Parameters")
    param_frame.pack(padx=10, pady=10, fill="x")

    # 問題データ設定用のフレーム
    data_source_frame = ttk.LabelFrame(scrollable_frame, text="Data Source")
    data_source_frame.pack(padx=10, pady=10, fill="x")

    # ナップザックデータの表示用フレーム
    data_display_frame = ttk.LabelFrame(scrollable_frame, text="Knapsack Data (Values and Weights)")
    data_display_frame.pack(padx=10, pady=10, fill="x")

    # GAの進捗グラフ表示用フレーム
    graph_frame = ttk.LabelFrame(scrollable_frame, text="GA Progress")
    graph_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # GAの結果表示用フレーム
    result_frame = ttk.LabelFrame(scrollable_frame, text="Results")
    result_frame.pack(padx=10, pady=10, fill="x")

    # GAパラメータ用のウィジェット
    ttk.Label(param_frame, text="Runs:").pack(side="left", padx=5)
    runs_entry = ttk.Entry(param_frame, width=5)
    runs_entry.insert(0, "5")
    runs_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Items Size:").pack(side="left", padx=5)
    items_entry = ttk.Entry(param_frame, width=5)
    items_entry.insert(0, "100")
    items_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Population Size:").pack(side="left", padx=5)
    pop_size_entry = ttk.Entry(param_frame, width=5)
    pop_size_entry.insert(0, "50")
    pop_size_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Generations:").pack(side="left", padx=5)
    generation_entry = ttk.Entry(param_frame, width=5)
    generation_entry.insert(0, "100")
    generation_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Crossover Rate:").pack(side="left", padx=5)
    crossover_entry = ttk.Entry(param_frame, width=5)
    crossover_entry.insert(0, "1")
    crossover_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Mutation Rate:").pack(side="left", padx=5)
    mutation_entry = ttk.Entry(param_frame, width=5)
    mutation_entry.insert(0, "0.01")
    mutation_entry.pack(side="left", padx=5)

    ttk.Label(param_frame, text="Capacity:").pack(side="left", padx=5)
    capacity_entry = ttk.Entry(param_frame, width=5)
    capacity_entry.insert(0, "1000")
    capacity_entry.pack(side="left", padx=5)

    # 問題のパラメータ用
    ttk.Label(data_source_frame, text="v_min:").pack(side="left", padx=5)
    vmin_entry = ttk.Entry(data_source_frame, width=5)
    vmin_entry.insert(0, "1")
    vmin_entry.pack(side="left", padx=5)

    ttk.Label(data_source_frame, text="v_max:").pack(side="left", padx=5)
    vmax_entry = ttk.Entry(data_source_frame, width=5)
    vmax_entry.insert(0, "100")
    vmax_entry.pack(side="left", padx=5)

    ttk.Label(data_source_frame, text="w_min:").pack(side="left", padx=5)
    wmin_entry = ttk.Entry(data_source_frame, width=5)
    wmin_entry.insert(0, "1")
    wmin_entry.pack(side="left", padx=5)

    ttk.Label(data_source_frame, text="w_max:").pack(side="left", padx=5)
    wmax_entry = ttk.Entry(data_source_frame, width=5)
    wmax_entry.insert(0, "50")
    wmax_entry.pack(side="left", padx=5)


    # データソース設定用のラジオボタン
    data_source_var = tk.StringVar(value="auto")
    
    def browse_file():
        global file_path
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            file_label.config(text=f"File: {file_path}")

    ttk.Radiobutton(data_source_frame, text="自動生成", variable=data_source_var, value="auto").pack(side="left", padx=5, pady=5)
    ttk.Radiobutton(data_source_frame, text="ファイルから読み込み", variable=data_source_var, value="file").pack(side="left", padx=5, pady=5)
    file_button = ttk.Button(data_source_frame, text="参照", command=browse_file)
    file_button.pack(side="left", padx=5, pady=5)
    file_label = ttk.Label(data_source_frame, text="File: (None)")
    file_label.pack(side="left", padx=5)

    # ナップザックデータ表示用のウィジェット
    ttk.Label(data_display_frame, text="Values:").pack(side="left", padx=5)
    values_text = tk.Text(data_display_frame, height=5, width=30)
    values_text.pack(side="left", padx=5, pady=5)

    ttk.Label(data_display_frame, text="Weights:").pack(side="left", padx=5)
    weights_text = tk.Text(data_display_frame, height=5, width=30)
    weights_text.pack(side="left", padx=5, pady=5)

    # 結果表示用のウィジェット
    result_text = tk.StringVar()
    result_label = ttk.Label(result_frame, textvariable=result_text)
    result_label.pack(padx=10, pady=10)

    # GAの実行ロジック
    def run_ga():
        """GUIからパラメータを取得し、GAを実行、結果を表示する関数です。"""
        try:
            num_runs = int(runs_entry.get())
            items_size = int(items_entry.get())
            population_size = int(pop_size_entry.get())
            generations_size = int(generation_entry.get())
            crossover_rate = float(crossover_entry.get())
            mutation_rate = float(mutation_entry.get())
            capacity = int(capacity_entry.get())
            v_min = int(vmin_entry.get())
            v_max = int(vmax_entry.get())
            w_min = int(wmin_entry.get())
            w_max = int(wmax_entry.get())
        except ValueError:
            result_text.set("Invalid input. Please enter numbers.")
            return

        # データの取得方法を決定
        data_source = data_source_var.get()
        if data_source == "auto":
            values = np.random.randint(v_min, v_max, size=items_size)
            weights = np.random.randint(w_min, w_max, size=items_size)
        else:
            if not file_path:
                result_text.set("Error: Please select a data file.")
                return
            
            try:
                data = np.loadtxt(file_path, dtype=int)
                if data.ndim == 1:
                    data = data.reshape(-1, 2)
                values = data[:, 0]
                weights = data[:, 1]
                items_entry.delete(0, tk.END)
                items_entry.insert(0, str(len(values)))
            except Exception as e:
                result_text.set(f"Error loading file: {e}")
                return

        # GAのサブ関数群
        def initialize_population(size, num_items, previous_best=None):
            population = np.random.randint(2, size=(size, num_items))
            return population

        def evaluate_fitness(population, values):
            total_values = np.sum(population * values, axis=1)
            return total_values

        def repair(population, weights, values, capacity_limit):
            num_individuals, _ = population.shape
            for i in range(num_individuals):
                individual = population[i]
                total_weight = np.sum(individual * weights)
                if total_weight <= capacity_limit:
                    continue
                value_density = values / weights
                selected_indices = np.where(individual == 1)[0]
                sorted_indices = selected_indices[np.argsort(value_density[selected_indices])]
                for idx in sorted_indices:
                    if total_weight <= capacity_limit:
                        break
                    individual[idx] = 0
                    total_weight -= weights[idx]
            return population

        def crossover(parent1, parent2):
            point = np.random.randint(1, len(parent1) - 1)
            child1 = np.concatenate([parent1[:point], parent2[point:]])
            child2 = np.concatenate([parent2[:point], parent1[point:]])
            return child1, child2

        def mutate(individual, mutation_rate):
            for i in range(len(individual)):
                if np.random.rand() < mutation_rate:
                    individual[i] = 1 - individual[i]
            return individual

        def genetic_algorithm(weights, values, capacity_limit, previous_best=None):
            population = initialize_population(population_size, len(values), previous_best)
            best_values_per_generation = []
            for _ in range(generations_size):
                repair(population, weights, values, capacity_limit)
                fitness = evaluate_fitness(population, values)
                sorted_indices = np.argsort(-fitness)
                population = population[sorted_indices]
                fitness = fitness[sorted_indices]
                new_population = population[:5]
                while len(new_population) < population_size:
                    parents = np.random.choice(population_size, 4, replace=False)
                    parent1_idx = parents[0] if fitness[parents[0]] >= fitness[parents[1]] else parents[1]
                    parent2_idx = parents[2] if fitness[parents[2]] >= fitness[parents[3]] else parents[3]
                    
                    if np.random.rand() < crossover_rate:
                        child1, child2 = crossover(population[parent1_idx], population[parent2_idx])
                    else:
                        child1, child2 = population[parent1_idx], population[parent2_idx]
                    
                    new_population = np.vstack([new_population, mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
                population = new_population
                best_values_per_generation.append(np.sum(values[population[0] == 1]))
            
            repair(population, weights, values, capacity_limit)
            fitness = evaluate_fitness(population, values)
            sorted_indices = np.argsort(-fitness)
            population = population[sorted_indices]

            best_individual = population[0]
            total_value = np.sum(values[best_individual == 1])
            total_weight = np.sum(weights[best_individual == 1])
            return best_individual, total_value, total_weight, best_values_per_generation

        def ga(values, weights, capacity):
            TTT = []
            all_best_values = []
            for _ in range(num_runs):
                best_individual, _, _, best_values = genetic_algorithm(weights, values, capacity)
                TTT.append(best_individual)
                all_best_values.append(best_values)
            
            value_TTT = [np.sum(values * element) for element in TTT]
            max_value_element = TTT[np.argmax(value_TTT)]
            total_value = np.sum(values * max_value_element)
            total_weight = np.sum(weights * max_value_element)
            
            return total_weight, total_value, all_best_values

        # データをGUIに表示
        values_text.delete("1.0", tk.END)
        values_text.insert(tk.END, np.array2string(values, separator=', '))
        
        weights_text.delete("1.0", tk.END)
        weights_text.insert(tk.END, np.array2string(weights, separator=', '))

        # GAを実行し、結果と世代ごとの最良値を表示用に取得
        final_weight, final_value, all_best_values = ga(values, weights, capacity)

        # グラフをクリア
        for widget in graph_frame.winfo_children():
            widget.destroy()
        
        # グラフを作成してGUIに埋め込む
        fig, ax = plt.subplots(figsize=(6, 4))
        for best_values in all_best_values:
            ax.plot(best_values)
        
        ax.set_title("Value per Generation over multiple runs")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Best Value")
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
        # 最終結果をGUIに表示
        result_text.set(f"Final Value: {final_value}\nFinal Weight: {final_weight}")

    # GUIの実行ボタン
    run_button = ttk.Button(
    scrollable_frame, 
    text="Run GA", 
    command=run_ga)
    run_button.pack(pady=10)

    # 終了ボタン
    quit_button = tk.Button(
    scrollable_frame,
    text="終了",
    fg="red",
    bg="white",
    activebackground="#aa0000",
    command=root.destroy
    )
    quit_button.pack(pady=30)

    #終了メニューバーボタン
    menubar = tk.Menu(root)
    root.configure(menu=menubar)
    menubar.add_command(label="終了", underline=0, command=root.quit)

    # メインループの開始
    root.mainloop()

if __name__ == "__main__":
    create_gui()
    