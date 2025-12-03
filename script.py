import os
from statistics import mean, median
import matplotlib.pyplot as plt


with open('nazwy_plikow_illumina', 'r') as illumina:
    for i in illumina:
        file_name = i.strip()
        print(f'ilosc odczytow w pliku {file_name}')
        os.system(f"grep -c '^@E' '{file_name}'")

with open('nazwy_plikow_nanopore', 'r') as nanopore:
    for n in nanopore:
        file_name = n.strip()
        totals = 0
        lengths = []
        prev = None
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if prev is not None and prev.startswith('@'):
                    dlugosc_odczytu = len(line)
                    totals += dlugosc_odczytu
                    lengths.append(dlugosc_odczytu)
                prev = line
        print(f"{file_name} Średnia dlugosc odczytu: {mean(lengths):.2f}")
        med = median(lengths)
        print(f"{file_name} Mediana dlugosci odczytu: {med:.2f}")
print(f"ilosc nugleotydow nanopore: {totals}")
with open('nazwy_plikow_razem', 'r') as pliki_razem:
    for file_name in pliki_razem:
        file_name = file_name.strip()
        gc_content = []
        lengths = []
        prev = None
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if prev is not None and prev.startswith('@'):
                    total = len(line)
                    lengths.append(total)
                    g = line.count('G') + line.count('g')
                    c = line.count('C') + line.count('c')
                    gc = ((g + c) / total) * 100 if total > 0 else 0
                    gc_content.append(gc)
                prev = line
        gc_mean_content = mean(gc_content)
        print(f"{file_name} Średnia GC: {gc_mean_content:.2f}%")

        plt.hist(lengths, bins=50, edgecolor='black')
        plt.title("Rozkład długości odczytów FASTQ")
        plt.xlabel("Długość odczytu")
        plt.ylabel("Liczba odczytów")

        outname = f"{os.path.basename(file_name)}_hist.png"
        plt.savefig(outname, dpi=300)
        plt.clf()

        print(f"Zapisano wykres: {outname}")
