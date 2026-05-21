from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# Configurar margens
sections = doc.sections
for section in sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(3)

# ============================================================
# CAPA
# ============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("UNIVERSIDADE PRESBITERIANA MACKENZIE")
run.bold = True
run.font.size = Pt(14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Faculdade de Computação e Informática")
run.font.size = Pt(12)

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Projeto Prático 2 (LAB2)")
run.bold = True
run.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Analisador Paralelo de Logs de CDN com OpenMP")
run.font.size = Pt(13)

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Relatório Técnico")
run.font.size = Pt(12)

for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Aluno: [PREENCHER NOME]")
run.font.size = Pt(11)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("TIA: [PREENCHER TIA]")
run.font.size = Pt(11)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Prof. Dr. Jean M. Laine")
run.font.size = Pt(11)

doc.add_page_break()

# ============================================================
# 1. METODOLOGIA
# ============================================================
doc.add_heading("1. Metodologia", level=1)

doc.add_paragraph(
    "Este relatório apresenta os resultados experimentais do Projeto Prático 2 (LAB2), "
    "cujo objetivo é implementar e comparar diferentes estratégias de sincronização "
    "para um analisador paralelo de logs de CDN utilizando OpenMP em linguagem C."
)

doc.add_paragraph(
    "Foram implementadas 5 versões do analisador:"
)

items = [
    "analyzer_seq — versão sequencial (baseline de corretude e desempenho);",
    "analyzer_par_critical — paralelização com #pragma omp critical (granularidade grossa);",
    "analyzer_par_atomic — paralelização com #pragma omp atomic update (instruções atômicas de hardware);",
    "analyzer_par_lock — paralelização com bucket locks independentes (granularidade média);",
    "analyzer_par_atomic_padded — variante atômica com padding na struct CacheNode (uma linha de cache por nó) para mitigar false sharing (Experimento C).",
]
for item in items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_paragraph(
    "Cada versão foi executada sobre dois arquivos de log distintos:"
)
items2 = [
    "log_distribuido.txt — acessos aproximadamente uniformes, baixa contenção;",
    "log_concorrente.txt — ~90% das requisições concentradas em poucas URLs, alta contenção.",
]
for item in items2:
    doc.add_paragraph(item, style='List Bullet')

doc.add_paragraph(
    "As métricas coletadas foram: tempo de execução, speedup, IPC (Instructions Per Cycle), "
    "cache misses e system time, obtidas via ferramentas de profiling (perf stat)."
)

doc.add_paragraph(
    "A validação de corretude foi realizada comparando o arquivo results.csv gerado "
    "por cada versão com o gabarito fornecido, utilizando sort + diff -s."
)

# ============================================================
# 2. AMBIENTE EXPERIMENTAL
# ============================================================
doc.add_heading("2. Ambiente Experimental", level=1)

doc.add_paragraph("[PREENCHER COM AS INFORMAÇÕES DO SEU AMBIENTE]")

table = doc.add_table(rows=8, cols=2)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = [
    ("Componente", "Especificação"),
    ("Sistema Operacional", "[preencher]"),
    ("Processador", "[preencher - modelo, núcleos, threads]"),
    ("Memória RAM", "[preencher]"),
    ("Cache L1/L2/L3", "[preencher]"),
    ("Compilador", "[preencher - gcc versão]"),
    ("Flags de compilação", "-Wall -Wextra -O2 -fopenmp"),
    ("Número de threads OpenMP", "[preencher]"),
]
for i, (col1, col2) in enumerate(headers):
    row = table.rows[i]
    row.cells[0].text = col1
    row.cells[1].text = col2
    if i == 0:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

# ============================================================
# 3. RESULTADOS - TABELAS
# ============================================================
doc.add_heading("3. Resultados Experimentais", level=1)

doc.add_heading("3.1 Tempo de Execução", level=2)

doc.add_paragraph("[PREENCHER — inserir tabela com tempos medidos para cada versão e cada log]")

table = doc.add_table(rows=6, cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row = table.rows[0]
header_row.cells[0].text = "Versão"
header_row.cells[1].text = "log_distribuido (s)"
header_row.cells[2].text = "log_concorrente (s)"
header_row.cells[3].text = "Total (s)"
for cell in header_row.cells:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

versions = ["Sequential", "Critical", "Atomic", "Bucket Lock", "Atomic + Padding"]
for i, v in enumerate(versions):
    table.rows[i+1].cells[0].text = v
    table.rows[i+1].cells[1].text = "[preencher]"
    table.rows[i+1].cells[2].text = "[preencher]"
    table.rows[i+1].cells[3].text = "[preencher]"

doc.add_heading("3.2 Speedup", level=2)

doc.add_paragraph("[PREENCHER — speedup = tempo_seq / tempo_paralelo]")

table = doc.add_table(rows=5, cols=3)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row = table.rows[0]
header_row.cells[0].text = "Versão"
header_row.cells[1].text = "Speedup (distribuído)"
header_row.cells[2].text = "Speedup (concorrente)"
for cell in header_row.cells:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

versions_par = ["Critical", "Atomic", "Bucket Lock", "Atomic + Padding"]
for i, v in enumerate(versions_par):
    table.rows[i+1].cells[0].text = v
    table.rows[i+1].cells[1].text = "[preencher]"
    table.rows[i+1].cells[2].text = "[preencher]"

doc.add_heading("3.3 Métricas de Hardware (perf stat)", level=2)

doc.add_paragraph("[PREENCHER — inserir métricas coletadas com perf stat para cada versão]")

table = doc.add_table(rows=6, cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row = table.rows[0]
header_row.cells[0].text = "Versão"
header_row.cells[1].text = "IPC"
header_row.cells[2].text = "Cache Misses"
header_row.cells[3].text = "System Time (s)"
for cell in header_row.cells:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

for i, v in enumerate(["Sequential", "Critical", "Atomic", "Bucket Lock", "Atomic + Padding"]):
    table.rows[i+1].cells[0].text = v
    table.rows[i+1].cells[1].text = "[preencher]"
    table.rows[i+1].cells[2].text = "[preencher]"
    table.rows[i+1].cells[3].text = "[preencher]"

doc.add_heading("3.4 Experimento C — False Sharing (Atomic vs Atomic + Padding)", level=2)

doc.add_paragraph(
    "Este experimento compara duas variantes paralelas que utilizam #pragma omp atomic update: "
    "a versão padrão (analyzer_par_atomic), onde a struct CacheNode tem layout compacto e "
    "diferentes hit_counts podem dividir a mesma linha de cache (64 bytes), e a versão padded "
    "(analyzer_par_atomic_padded), onde cada nó é alinhado a uma linha de cache completa por meio "
    "de um campo padding[5] do tipo long, eliminando false sharing entre contadores."
)

doc.add_paragraph(
    "A struct utilizada na versão padded é:"
)
doc.add_paragraph(
    "typedef struct PaddedCacheNode {\n"
    "    char *url;\n"
    "    long hit_count;\n"
    "    struct PaddedCacheNode *next;\n"
    "    long padding[5];\n"
    "} PaddedCacheNode;",
    style='Intense Quote'
)
doc.add_paragraph(
    "Em x86_64 isso totaliza exatamente 64 bytes por nó, garantindo que cada hit_count resida em "
    "uma linha de cache exclusiva."
)

doc.add_paragraph(
    "O dataset utilizado é log_concorrente.txt, onde ~90% das requisições concentram-se em poucas "
    "URLs (hotspots). Esse cenário maximiza o efeito de false sharing, pois várias threads "
    "atualizam frequentemente contadores fisicamente próximos na memória. As métricas foram "
    "coletadas com perf stat -e cache-references,cache-misses."
)

doc.add_paragraph("[PREENCHER — inserir métricas comparativas coletadas com perf stat]")

table = doc.add_table(rows=3, cols=5)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row = table.rows[0]
header_row.cells[0].text = "Versão"
header_row.cells[1].text = "Tempo (s)"
header_row.cells[2].text = "Cache References"
header_row.cells[3].text = "Cache Misses"
header_row.cells[4].text = "Miss Rate (%)"
for cell in header_row.cells:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True

for i, v in enumerate(["Atomic (sem padding)", "Atomic + Padding"]):
    table.rows[i+1].cells[0].text = v
    table.rows[i+1].cells[1].text = "[preencher]"
    table.rows[i+1].cells[2].text = "[preencher]"
    table.rows[i+1].cells[3].text = "[preencher]"
    table.rows[i+1].cells[4].text = "[preencher]"

doc.add_paragraph(
    "Tradeoff de memória: a versão padded aumenta o consumo de memória da tabela hash "
    "(aproximadamente 64 bytes por nó vs ~24 bytes na versão compacta). Com 100.000 URLs, "
    "isso representa ~6,4 MB no total — perfeitamente aceitável para o ganho de desempenho "
    "esperado em cenários de alta contenção."
)

# ============================================================
# 4. GRAFICOS
# ============================================================
doc.add_heading("4. Gráficos", level=1)

doc.add_paragraph("[PREENCHER — inserir gráficos comparativos]")
doc.add_paragraph("Sugestões de gráficos:")
items_graficos = [
    "Gráfico de barras: Tempo de execução por versão (agrupado por log)",
    "Gráfico de barras: Speedup por versão",
    "Gráfico de barras: Cache misses por versão",
    "Gráfico de barras: IPC por versão",
    "Gráfico de barras: Cache misses — Atomic vs Atomic + Padding (Experimento C)",
]
for item in items_graficos:
    doc.add_paragraph(item, style='List Bullet')

# ============================================================
# 5. QUESTOES DE ANALISE
# ============================================================
doc.add_heading("5. Questões de Análise", level=1)

# Q1
doc.add_heading("Q1: Por que a versão critical pode degradar sob alta contenção?", level=2)
doc.add_paragraph(
    "A diretiva #pragma omp critical cria uma única região crítica global. Isso significa que, "
    "independentemente de qual URL está sendo acessada, TODAS as threads precisam esperar pela "
    "mesma trava para incrementar qualquer contador."
)
doc.add_paragraph(
    "Quando há alta contenção (como no log_concorrente.txt, onde 90% dos acessos se concentram "
    "em poucas URLs), o problema se agrava:"
)
items_q1 = [
    "Apenas uma thread executa o incremento por vez, enquanto todas as outras ficam bloqueadas.",
    "O paralelismo efetivo é praticamente eliminado — o programa se comporta quase como sequencial.",
    "O custo de espera cresce linearmente com o número de threads.",
    "Há overhead adicional do SO para gerenciar a fila de threads bloqueadas (context switches).",
]
for item in items_q1:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph(
    "Em resumo: a granularidade grossa da sincronização transforma o gargalo lógico "
    "(poucas URLs populares) em um gargalo físico (todas as threads disputam um único lock), "
    "causando serialização e degradação de desempenho."
)

# Q2
doc.add_heading("Q2: Como locks por bucket equilibram sincronização e paralelismo?", level=2)
doc.add_paragraph(
    "A estratégia de bucket lock atribui um lock independente (omp_lock_t) para cada bucket "
    "da tabela hash."
)
doc.add_paragraph("Sincronização:")
items_q2a = [
    "Threads que acessam a mesma URL (ou URLs no mesmo bucket) ainda esperam uma pela outra, garantindo corretude.",
    "Não há condição de corrida porque o lock protege todo o bucket.",
]
for item in items_q2a:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("Paralelismo:")
items_q2b = [
    "Threads que acessam URLs em buckets diferentes executam simultaneamente sem bloqueio.",
    "Com 131.071 buckets, a probabilidade de colisão é muito baixa no cenário distribuído.",
]
for item in items_q2b:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph(
    "O resultado é uma granularidade média: mais paralela que critical, mais simples que "
    "estruturas lock-free, e com boa escalabilidade."
)

# Q3
doc.add_heading("Q3: Compare cache misses entre versões atomic e padded.", level=2)
doc.add_paragraph("Versão Atomic (sem padding):")
items_q3a = [
    "Campos hit_count de diferentes CacheNodes podem residir na mesma linha de cache (64 bytes).",
    "Atualizações atômicas invalidam a linha inteira em todos os núcleos (false sharing).",
    "Resultado: alto número de cache misses, especialmente L1d.",
]
for item in items_q3a:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("Versão Padded (com padding):")
items_q3b = [
    "Cada CacheNode é alinhado para ocupar uma linha de cache completa.",
    "Atualizações em um hit_count NÃO invalidam linhas de outros hit_counts.",
    "Resultado: redução significativa de cache misses e maior throughput.",
]
for item in items_q3b:
    doc.add_paragraph(item, style='List Bullet')

doc.add_paragraph("[PREENCHER — inserir dados comparativos de cache misses obtidos via perf stat]")

# Q4
doc.add_heading("Q4: Houve speedup superlinear?", level=2)
doc.add_paragraph("[PREENCHER — com base nos resultados medidos, responder se houve ou não]")
doc.add_paragraph(
    "Speedup superlinear (S(p) > p) pode ocorrer quando a soma das caches de múltiplos "
    "núcleos permite que o dataset caiba em cache, algo impossível com um único núcleo. "
    "Também pode ocorrer por melhor utilização do prefetcher com acessos mais localizados por thread."
)
doc.add_paragraph("Causas possíveis caso tenha ocorrido:")
items_q4 = [
    "Efeito de cache agregado (soma das caches L1/L2 de múltiplos núcleos).",
    "Melhor localidade por thread devido ao particionamento do trabalho.",
    "Prefetching mais eficiente com acessos mais previsíveis.",
]
for item in items_q4:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("Causas caso NÃO tenha ocorrido:")
items_q4b = [
    "Overhead de sincronização (locks, atomics).",
    "Contenção em buckets populares.",
    "Limitações de largura de banda de memória.",
]
for item in items_q4b:
    doc.add_paragraph(item, style='List Bullet')

# Q5
doc.add_heading("Q5: Quando o aumento de memória causado pelo padding torna-se vantajoso?", level=2)
doc.add_paragraph("O padding se torna vantajoso quando:")
items_q5 = [
    "Há alta contenção em nós próximos na memória (múltiplas threads atualizando hit_counts na mesma linha de cache).",
    "O número de threads é elevado (com mais threads, cada invalidação afeta mais núcleos).",
    "O workload é CPU-bound e não memory-bound.",
    "O dataset cabe em memória mesmo com o padding (100.000 URLs × 64 bytes ≈ 6.4 MB — aceitável).",
]
for item in items_q5:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("NÃO é vantajoso quando:")
items_q5b = [
    "Poucas threads (1-2): false sharing é mínimo.",
    "Acessos muito distribuídos: baixa probabilidade de colisão na mesma linha.",
    "Workload memory-bound: o aumento de footprint piora a pressão no cache.",
]
for item in items_q5b:
    doc.add_paragraph(item, style='List Bullet')

# Q6
doc.add_heading("Q6: Qual solução seria utilizada em uma CDN real?", level=2)
doc.add_paragraph(
    "Em uma CDN real (Netflix, Cloudflare, Akamai), a solução seria significativamente "
    "mais sofisticada:"
)
doc.add_paragraph("Estruturas de dados:")
items_q6a = [
    "Tabelas hash concorrentes lock-free (CAS - Compare-And-Swap).",
    "Contadores thread-local com merge periódico (zero contenção no caminho crítico).",
    "Bloom filters para pré-filtragem rápida.",
]
for item in items_q6a:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("Arquitetura:")
items_q6b = [
    "Processamento distribuído (múltiplas máquinas, não apenas threads).",
    "Sistemas de streaming (Apache Kafka + Flink/Spark Streaming).",
    "Contadores aproximados (HyperLogLog, Count-Min Sketch) quando precisão exata não é necessária.",
]
for item in items_q6b:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph(
    "A versão bucket lock do projeto é a que mais se aproxima de sistemas reais, "
    "pois o conceito de 'lock por partição' é amplamente usado em bancos de dados e caches concorrentes."
)

# Q7
doc.add_heading("Q7: Como listas encadeadas impactam localidade de cache?", level=2)
doc.add_paragraph("Impacto negativo na localidade espacial:")
items_q7a = [
    "Nós alocados com malloc() em momentos diferentes resultam em endereços não contíguos.",
    "Cada ponteiro 'next' pode apontar para região completamente diferente da memória.",
    "O prefetcher de hardware não consegue prever o próximo endereço (pointer chasing).",
    "Cada acesso a um nó pode causar um cache miss.",
]
for item in items_q7a:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph("Alternativas usadas em sistemas reais:")
items_q7b = [
    "Open addressing (linear probing): elementos no próprio array, excelente localidade.",
    "Memory pools: nós alocados em blocos contíguos.",
    "Robin Hood hashing / Cuckoo hashing: busca O(1) com boa localidade.",
]
for item in items_q7b:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph(
    "No contexto do projeto, o impacto é mitigado pelo tamanho grande da tabela (131.071 buckets), "
    "resultando em listas muito curtas (média de ~0.76 nós por bucket com 100.000 URLs)."
)

# ============================================================
# 6. ANALISE CRITICA
# ============================================================
doc.add_heading("6. Análise Crítica", level=1)

doc.add_paragraph("[PREENCHER — com base nos resultados obtidos, elaborar análise crítica abordando:]")
items_critica = [
    "Qual versão apresentou melhor desempenho em cada cenário (distribuído vs concorrente)?",
    "Os resultados confirmam a teoria sobre granularidade de sincronização?",
    "O impacto do false sharing foi observável nas métricas?",
    "A escolha do tamanho da tabela hash influenciou os resultados?",
    "Quais foram as limitações do experimento?",
]
for item in items_critica:
    doc.add_paragraph(item, style='List Bullet')

# ============================================================
# 7. CONCLUSAO
# ============================================================
doc.add_heading("7. Conclusão", level=1)

doc.add_paragraph("[PREENCHER — resumir as principais descobertas e aprendizados:]")
items_conclusao = [
    "Resumo dos resultados principais.",
    "Relação entre granularidade de sincronização e desempenho.",
    "Importância da escolha da estratégia de acordo com o padrão de acesso.",
    "Aplicabilidade dos conceitos em sistemas reais.",
]
for item in items_conclusao:
    doc.add_paragraph(item, style='List Bullet')

# ============================================================
# SALVAR
# ============================================================
output_path = "Relatorio_LAB2.docx"
doc.save(output_path)
print(f"Relatório salvo em: {output_path}")
