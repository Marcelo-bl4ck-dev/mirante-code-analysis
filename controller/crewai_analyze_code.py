from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import litellm

# Agente responsável por buscar recomendações de melhorias em código Python
code_analyzer = Agent(
    role='Analista de Código Python',
    goal='Avaliar códigos Python e fornecer sugestões factualmente corretas para melhorar performance, '
         'corrigir vulnerabilidades de segurança e aprimorar a legibilidade.',
    backstory='Um especialista em análise de código, com experiência em otimização e segurança, '
               'capaz de detectar padrões ineficientes e vulnerabilidades ocultas no código {code}. '
               'Seu foco é identificar melhorias e justificar cada recomendação de forma clara e técnica. '
               'As informações coletadas serão utilizadas pelo agente Code Implementer para aprimorar o código.',
    allow_code_execution=True,
    verbose=True
)

# Agente responsável por implementar as melhorias sugeridas
code_implementer = Agent(
    role='Desenvolvedor de Código Python',
    goal='Aplicar as recomendações do code_analyzer para gerar um código otimizado, seguro e bem estruturado.',
    backstory=('Um engenheiro de software experiente, especializado em Python, '
               'com foco em performance, segurança e boas práticas de desenvolvimento. '
               'Ele recebe sugestões do code_analyzer e implementa as mudanças necessárias, '
               'garantindo que o código final seja eficiente, seguro e de fácil manutenção.'),
    allow_code_execution=True,
    verbose=True
)

# Agente responsável por documentar a análise e as melhorias
report_builder = Agent(
    role='Gerador de Relatórios de Análise de Código',
    goal='Criar um relatório detalhado com as recomendações do code_analyzer e '
         'as alterações feitas pelo code_implementer, servindo como histórico técnico.',
    backstory=('Um analista meticuloso especializado em documentação técnica, '
               'responsável por gerar relatórios claros e organizados. '
               'Ele coleta as informações da análise inicial e das implementações feitas, '
               'compilando tudo em um documento que pode ser utilizado para auditorias, aprendizado e rastreabilidade.'),
    allow_code_execution=False,
    verbose=True
)

# Task 1: Analisar o código Python e gerar recomendações
analyze_code = Task(
    description='Analisar um código Python fornecido, identificando oportunidades de melhoria '
                'em termos de performance, segurança e boas práticas.',
    expected_output='Uma lista detalhada de recomendações, incluindo melhorias de performance, '
                    'correção de vulnerabilidades e justificativas técnicas para cada sugestão.',
    agent=code_analyzer
)

# Task 2: Implementar as melhorias sugeridas
implement_suggestions = Task(
    description='Com base nas recomendações do code_analyzer, gerar um novo código Python '
                'que incorpore as melhorias sugeridas, garantindo eficiência e segurança.',
    expected_output='Um código Python otimizado com as melhorias implementadas, '
                    'mantendo a clareza e a conformidade com as melhores práticas.',
    agent=code_implementer
)

# Task 3: Gerar um relatório detalhado da análise e das alterações realizadas
generate_report = Task(
    description='Compilar um relatório completo que documenta as recomendações do code_analyzer '
                'e as mudanças implementadas pelo code_implementer.',
    expected_output='Um relatório detalhado em formato de texto estruturado, contendo: '
                    '1. As recomendações de melhorias e suas justificativas, '
                    '2. As mudanças realizadas no código e por quê, '
                    '3. Um resumo técnico das melhorias aplicadas.',
    agent=report_builder
)

my_crew = Crew(
    agents=[code_analyzer, code_implementer, report_builder],
    tasks=[analyze_code, implement_suggestions, generate_report],
    process=Process.sequential,
    verbose=True
)

def crewai_analyze_code(code):
    crew_output = my_crew.kickoff(inputs={"code": str(code)})

    # Get a session
    session = db_instance.get_session()

    # Insert a record
    new_analysis = AnalysisHistory(
        code_snippet=f"{code}",
        suggestion=crew_output.raw["generate_report"]["output"]
    )

    session.add(new_analysis)
    session.commit()
    session.close()

    return crew_output.raw