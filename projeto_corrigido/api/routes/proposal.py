from flask import Blueprint, request, jsonify, render_template_string
import uuid
import json
import os
from datetime import datetime

proposal_bp = Blueprint('proposal', __name__)

# Armazenar propostas em memória (em produção, usar banco de dados)
proposals_storage = {}

@proposal_bp.route('/generate', methods=['POST'])
def generate_proposal():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['clientName', 'projectType']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Gerar ID único para a proposta
        proposal_id = str(uuid.uuid4())[:8]
        
        # Criar dados da proposta
        proposal_data = {
            'id': proposal_id,
            'clientName': data.get('clientName'),
            'clientEmail': data.get('clientEmail'),
            'clientPhone': data.get('clientPhone'),
            'companyName': data.get('companyName'),
            'projectType': data.get('projectType'),
            'projectDescription': data.get('projectDescription'),
            'budget': data.get('budget'),
            'timeline': data.get('timeline'),
            'objectives': data.get('objectives'),
            'createdAt': datetime.now().isoformat(),
            'createdDate': datetime.now().strftime('%d/%m/%Y')
        }
        
        # Armazenar proposta
        proposals_storage[proposal_id] = proposal_data
        
        return jsonify({
            'success': True,
            'proposalId': proposal_id,
            'url': f'/proposta/{proposal_id}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proposal_bp.route('/view/<proposal_id>')
def view_proposal(proposal_id):
    proposal = proposals_storage.get(proposal_id)
    if not proposal:
        return "Proposta não encontrada", 404
    
    # Template HTML da proposta
    template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposta Comercial - {{ proposal.companyName or proposal.clientName }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #000000 0%, #1e3a8a 50%, #000000 100%);
            color: white;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 40px;
        }
        
        .logo {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 24px;
        }
        
        .company-name {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            font-size: 1.2rem;
            color: #cbd5e1;
            margin-bottom: 30px;
        }
        
        .proposal-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .client-info {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 40px;
        }
        
        .section {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #3b82f6;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 8px;
        }
        
        .info-label {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .project-description {
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 8px;
            line-height: 1.6;
        }
        
        .plan-details {
            background: linear-gradient(45deg, rgba(59,130,246,0.1), rgba(29,78,216,0.1));
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
        }
        
        .plan-name {
            font-size: 1.5rem;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 15px;
        }
        
        .plan-features {
            list-style: none;
            margin: 15px 0;
        }
        
        .plan-features li {
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .plan-features li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
        }
        
        .investment {
            background: linear-gradient(45deg, rgba(16,185,129,0.1), rgba(34,197,94,0.1));
            border: 1px solid rgba(16,185,129,0.3);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin: 30px 0;
        }
        
        .investment-amount {
            font-size: 2.5rem;
            font-weight: bold;
            color: #10b981;
            margin-bottom: 10px;
        }
        
        .roi-info {
            color: #cbd5e1;
            margin-top: 15px;
        }
        
        .cta-section {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(45deg, rgba(59,130,246,0.1), rgba(29,78,216,0.1));
            border-radius: 16px;
            margin: 40px 0;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: transform 0.3s ease;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
        }
        
        .footer {
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #94a3b8;
        }
        
        @media (max-width: 768px) {
            .proposal-title {
                font-size: 2rem;
            }
            
            .company-name {
                font-size: 2rem;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .section {
            animation: fadeInUp 0.6s ease forwards;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">✨</div>
            <h1 class="company-name">Evolua Rio</h1>
            <p class="tagline">A sua Marca no topo</p>
            <h2 class="proposal-title">Proposta Comercial</h2>
        </header>
        
        <div class="client-info">
            <h3 class="section-title">Informações do Cliente</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Cliente</div>
                    <div class="info-value">{{ proposal.clientName }}</div>
                </div>
                {% if proposal.companyName %}
                <div class="info-item">
                    <div class="info-label">Empresa</div>
                    <div class="info-value">{{ proposal.companyName }}</div>
                </div>
                {% endif %}
                {% if proposal.clientEmail %}
                <div class="info-item">
                    <div class="info-label">Email</div>
                    <div class="info-value">{{ proposal.clientEmail }}</div>
                </div>
                {% endif %}
                {% if proposal.clientPhone %}
                <div class="info-item">
                    <div class="info-label">Telefone</div>
                    <div class="info-value">{{ proposal.clientPhone }}</div>
                </div>
                {% endif %}
                <div class="info-item">
                    <div class="info-label">Data da Proposta</div>
                    <div class="info-value">{{ proposal.createdDate }}</div>
                </div>
            </div>
        </div>
        
        {% if proposal.projectDescription %}
        <div class="section">
            <h3 class="section-title">Sobre o Projeto</h3>
            <div class="project-description">
                {{ proposal.projectDescription }}
            </div>
        </div>
        {% endif %}
        
        <div class="section">
            <h3 class="section-title">Solução Proposta</h3>
            
            {% if proposal.projectType == 'google-ads' %}
            <div class="plan-details">
                <div class="plan-name">Plano Google - Google Ads</div>
                <p>Ideal para empresas que querem dominar as buscas</p>
                <ul class="plan-features">
                    <li>Gestão Estratégica de Google Ads</li>
                    <li>Landing Page de Alta Conversão</li>
                    <li>Acompanhamento Comercial Básico</li>
                    <li>Apareça para quem já busca por seus produtos</li>
                    <li>Transforme visitantes em leads qualificados</li>
                    <li>Suporte para converter leads em vendas</li>
                </ul>
                <div class="investment">
                    <div class="investment-amount">R$ 1.700/mês</div>
                    <div class="roi-info">ROI médio de 3x o investimento em 90 dias</div>
                </div>
            </div>
            {% elif proposal.projectType == 'meta-ads' %}
            <div class="plan-details">
                <div class="plan-name">Plano Meta - Meta Ads</div>
                <p>Para empresas que querem dominar as redes sociais</p>
                <ul class="plan-features">
                    <li>Gestão de Tráfego Meta Ads</li>
                    <li>CRM para Gestão de Leads</li>
                    <li>Social Media Estratégico</li>
                    <li>Alcance seu público ideal nas redes sociais</li>
                    <li>Organize e acompanhe cada oportunidade</li>
                    <li>Construa autoridade e engajamento</li>
                </ul>
                <div class="investment">
                    <div class="investment-amount">R$ 1.747/mês</div>
                    <div class="roi-info">ROI médio de 2.8x o investimento em 90 dias</div>
                </div>
            </div>
            {% elif proposal.projectType == 'premium' %}
            <div class="plan-details">
                <div class="plan-name">Plano Premium - Solução Completa</div>
                <p>A solução completa para dominar o mercado digital</p>
                <ul class="plan-features">
                    <li>Gestão de Tráfego Google Ads + Meta Ads</li>
                    <li>CRM Completo com Automação</li>
                    <li>Inteligência Artificial Aplicada</li>
                    <li>Landing Page + Social Media Completo</li>
                    <li>Acompanhamento Comercial QUINZENAL</li>
                    <li>Encontro Comercial SEMANAL</li>
                    <li>Construção/otimização do playbook de vendas</li>
                    <li>Consultoria comercial MENSAL</li>
                </ul>
                <div class="investment">
                    <div class="investment-amount">R$ 2.997/mês</div>
                    <div class="roi-info">ROI médio de 4x o investimento em 90 dias</div>
                </div>
            </div>
            {% else %}
            <div class="plan-details">
                <div class="plan-name">Consultoria Personalizada</div>
                <p>Solução customizada para suas necessidades específicas</p>
                <ul class="plan-features">
                    <li>Análise completa do seu negócio</li>
                    <li>Estratégia personalizada</li>
                    <li>Implementação sob medida</li>
                    <li>Acompanhamento dedicado</li>
                </ul>
            </div>
            {% endif %}
        </div>
        
        <div class="section">
            <h3 class="section-title">O Método VENCI</h3>
            <p style="margin-bottom: 20px; line-height: 1.6;">
                Nossa metodologia exclusiva que une ciência e estratégia para transformar a forma como você vende.
            </p>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">VENDAS</div>
                    <div class="info-value">Foco total na conversão e aumento do faturamento</div>
                </div>
                <div class="info-item">
                    <div class="info-label">ESTRATÉGIA</div>
                    <div class="info-value">Estrutura clara para crescimento previsível</div>
                </div>
                <div class="info-item">
                    <div class="info-label">NEUROCIÊNCIA</div>
                    <div class="info-value">Aplicamos princípios da ciência para aumentar conversões</div>
                </div>
                <div class="info-item">
                    <div class="info-label">COMUNICAÇÃO</div>
                    <div class="info-value">Histórias que conectam a nível emocional</div>
                </div>
                <div class="info-item">
                    <div class="info-label">INTELIGÊNCIA ARTIFICIAL</div>
                    <div class="info-value">IA aplicada ao seu negócio para otimização</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Por que escolher a Evolua Rio?</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Metodologia Exclusiva</div>
                    <div class="info-value">Baseada em neurociência e storytelling</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Resultados Comprovados</div>
                    <div class="info-value">+1000 empresas transformadas</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Aumento Médio</div>
                    <div class="info-value">+30% na taxa de conversão</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Redução Média</div>
                    <div class="info-value">-25% no custo de aquisição</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Experiência Comprovada</div>
                    <div class="info-value">+R$ 10 milhões gerenciados em anúncios</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Crescimento Real</div>
                    <div class="info-value">+40% aumento médio no faturamento</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Depoimentos de Clientes</h3>
            <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <p style="font-style: italic; margin-bottom: 15px; line-height: 1.6;">
                    "A EVOLUA RIO transformou a forma como captamos leads. Em apenas 3 meses, vimos um aumento de 40% nas nossas vendas. O acompanhamento comercial é um diferencial incrível!"
                </p>
                <p style="font-weight: bold; color: #3b82f6;">José Eduardo - CEO Beauty Sorriso</p>
            </div>
            <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <p style="font-style: italic; margin-bottom: 15px; line-height: 1.6;">
                    "Estávamos perdidos na gestão de tráfego. A EVOLUA RIO nos trouxe leads muito mais qualificados e conseguiu reduzir nosso CAC em 25%. Recomendo a todos!"
                </p>
                <p style="font-weight: bold; color: #3b82f6;">Maria Oliveira - Diretora de vendas na Status Imóveis</p>
            </div>
            <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px;">
                <p style="font-style: italic; margin-bottom: 15px; line-height: 1.6;">
                    "Desde que começamos a trabalhar com a EVOLUA RIO, nossos resultados são visíveis. Além da expertise em tráfego, o suporte e a atenção da equipe são excepcionais."
                </p>
                <p style="font-weight: bold; color: #3b82f6;">Carlos Santos - Proprietário da Arquitetos e Cia</p>
            </div>
        </div>
        
        {% if proposal.objectives %}
        <div class="section">
            <h3 class="section-title">Objetivos do Projeto</h3>
            <div class="project-description">
                {{ proposal.objectives }}
            </div>
        </div>
        {% endif %}
        
        {% if proposal.timeline %}
        <div class="section">
            <h3 class="section-title">Cronograma</h3>
            <div class="info-item">
                <div class="info-label">Prazo de Implementação</div>
                <div class="info-value">{{ proposal.timeline }}</div>
            </div>
        </div>
        {% endif %}
        
        <div class="cta-section">
            <h3 style="margin-bottom: 20px;">Pronto para transformar seu negócio?</h3>
            <p style="margin-bottom: 30px; color: #cbd5e1;">
                Entre em contato conosco e comece sua jornada de crescimento hoje mesmo!
            </p>
            <a href="https://wa.me/5521964333304?text=Olá! Gostaria de saber mais sobre a proposta para {{ proposal.clientName }}" 
               class="cta-button" target="_blank">
                Falar com Especialista
            </a>
        </div>
        
        <footer class="footer">
            <p>&copy; 2024 Evolua Rio - Todos os direitos reservados</p>
            <p>Captação de Leads com Neurociência e Storytelling</p>
        </footer>
    </div>
</body>
</html>
    """
    
    return render_template_string(template, proposal=proposal)

