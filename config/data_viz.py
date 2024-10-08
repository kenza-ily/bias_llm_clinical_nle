import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import re
from itertools import combinations
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# LLMs lists
closed_llms = ['gpt3', 'gpt4o', 'gpt4turbo', 'haiku', 'sonnet3_5', 'gemini_3_5_flash']
open_llms = ['nvidia_llama3_1_403b', 'nvidia_llama3.70b']
llms_ft = ['gpt4omini_bsl','gpt4omini_ft','gpt4omini_ft2']
llms_ft_mcq=['gpt_bsl','gpt_ft','jallama_bsl','jallama_ft']
llms_ft_xpl=['gpt4omini_ft3_xpl','gpt4omini_ft3_xpl_bsl','jallama_xpl_bsl','jallama_xpl_ft']
llms_exp0 = ['gpt3']
llms_exp1 = ['gpt3', 'gpt4o', 'gpt4turbo']

# Colors
colors_llms = {
    # GPTs
    'gpt3': '#57A981', 
    'gpt4o': '#51DA4C', 
    'gpt4turbo': '#2D712A', 
    # Claude
    'haiku': '#D5A480', 
    'sonnet3_5': '#C97C5C', 
    # Gemini
    'gemini_3_5_flash': '#8479C7',
    # Llama
    'nvidia_llama3.70b': '#0081FB',
    'nvidia_llama3_1_403b': '#0064e0',
    # Fine tuned
    # GPT
    'gpt_bsl_mcq': '#FF00FF',
    'gpt_ft_mcq': '#C500C5',
    'gpt_bsl_xpl': '#B161FD',
    'gpt_ft_xpl': '#2A044EFF',
    # JALLaMA
    'jallama_bsl_mcq': '#D7F9E6',
    'jallama_ft_mcq': '#CDA000',
    'jallama_bsl_medqa': '#F9E67A',
    'jallama_ft_medqa': '#CDA000',
    'jallama_bsl_xpl': '#D71635',
    'jallama_ft_xpl': '#8B0018'
    }

colors_gender = {
    'male': '#3344FF',
    'male_original': '#3344FF',
    'male_augmented': '#848DF090',
    'female': '#C75FFF',
    'female_original': '#C75FFF',
    'female_augmented': '#FF5FF77D',
    'neutral': '#EDF98E',
    'neutral_augmented': '#CBCFAE'
}

version_colors = {
    'Arab - male': '#CC0000',
    'Arab - female': '#FF6666',
    'Arab - neutral': '#FF0000',
    'Asian - male': '#CC7A00',
    'Asian - female': '#FFCC66',
    'Asian - neutral': '#FFA500',
    'Black - male': '#CCCC00',
    'Black - female': '#FFFF66',
    'Black - neutral': '#FFFF00',
    'Hispanic - male': '#006600',
    'Hispanic - female': '#66CC66',
    'Hispanic - neutral': '#00FF00',
    'White - male': '#0000CC',
    'White - female': '#6699FF',
    'White - neutral': '#0000FF',
    'Mixed - male': '#660066',
    'Mixed - female': '#CC99FF',
    'Mixed - neutral': '#800080',
}

colors_ethnicity = {
    'Arab': '#FF0000',
    'Asian': '#FFA500',
    'Black': '#FFFF00',
    'Hispanic': '#00FF00',
    'White': '#0000FF',
    'Mixed': '#800080',
}

colors_version_binary = {
    'original': '#FFFFFF',
    'augmented': '#000000'
}

colors_performance = {
    1: '#00FF0078',
    0: '#FF000084'
}

colors_gender= {'male': '#90D5DD',
                'female': '#EC6D72',
                'neutral': '#56E11F79'}

# Graph Parameters
cmap_personalised = "YlOrRd"
figure_size = (10, 6)
fontsize_title = 20
label_fontsize = 16
legend_fontsize = 14
linewidth_wordcloud = 10

# Orders
order_version = ['original', 'augmented_Arab_male_frommale', 'augmented_Arab_female_frommale', 'augmented_Arab_neutral_frommale', 'augmented_Asian_male_frommale', 'augmented_Asian_female_frommale', 'augmented_Asian_neutral_frommale', 'augmented_Black_male_frommale', 'augmented_Black_female_frommale', 'augmented_Black_neutral_frommale', 'augmented_Hispanic_male_frommale', 'augmented_Hispanic_female_frommale', 'augmented_Hispanic_neutral_frommale', 'augmented_White_male_frommale', 'augmented_White_female_frommale', 'augmented_White_neutral_frommale', 'augmented_Mixed_male_frommale', 'augmented_Mixed_female_frommale', 'augmented_Mixed_neutral_frommale', 'augmented_Arab_male_fromfemale', 'augmented_Arab_female_fromfemale', 'augmented_Arab_neutral_fromfemale', 'augmented_Asian_male_fromfemale', 'augmented_Asian_female_fromfemale', 'augmented_Asian_neutral_fromfemale', 'augmented_Black_male_fromfemale', 'augmented_Black_female_fromfemale', 'augmented_Black_neutral_fromfemale', 'augmented_Hispanic_male_fromfemale', 'augmented_Hispanic_female_fromfemale', 'augmented_Hispanic_neutral_fromfemale', 'augmented_White_male_fromfemale', 'augmented_White_female_fromfemale', 'augmented_White_neutral_fromfemale', 'augmented_Mixed_male_fromfemale', 'augmented_Mixed_female_fromfemale', 'augmented_Mixed_neutral_fromfemale', 'original']

order_version_gender = ['original_male', 'augmented_male', 'original_female', 'augmented_female', 'original_neutral', 'augmented_neutral']

order_version_binary = ['original', 'augmented']

order_ethnicity = ['Arab', 'Asian', 'Black', 'Hispanic', 'White', 'Mixed']

order_gender = ['male', 'female', 'neutral']

order_version_gender_ethnicity = [f"{gender}_{version}_{ethnicity}" for gender in order_gender for version in order_version_binary for ethnicity in order_ethnicity]

def plot_llm_colors():
    fig, ax = plt.subplots(figsize=(8, 2))
    spacing = 3  # Adding 0.2 cm space between each color
    
    for i, (key, color) in enumerate(colors_llms.items()):
        ax.add_patch(plt.Rectangle((i * spacing, 0), 1, 1, color=color))  # Adjust position by spacing
        name = names_llms.get(key, key).replace('_', ' ')  # Use names_llms or fallback to key
        ax.text(i * spacing + 0.5, -0.1, name, ha='center', va='center', fontsize=6, color='black')
    
    ax.set_xlim(0, len(colors_llms) * spacing)
    ax.set_ylim(-0.5, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.show()



# ============== NAMES

names_llms = {
    # GPTs
    'gpt3': 'GPT-3',
    'gpt4o': 'GPT-4o',
    'gpt4turbo': 'GPT-4 Turbo',
    # Claude
    'haiku': 'Haiku',
    'sonnet3_5': 'Sonnet 3.5', 
    # Gemini
    'gemini_3_5_flash': 'Gemini 3.5 Flash',
    # Llama
    'nvidia_llama3.70b': 'Llama 3.70b',
    'nvidia_llama3_1_403b': 'Llama 3.1.403b',
    # Fine tuned
    'gpt_bsl_mcq': 'GPT MCQ | BSL',
    'gpt_ft_mcq': 'GPT MCQ | FT',
    'gpt_bsl_xpl': 'GPT XPL | BSL',
    'gpt_ft_xpl': 'GPT XPL | FT',
    # JALLaMA
    'jallama_bsl_mcq': 'Llama MCQ | BSL',
    'jallama_ft_mcq': 'Llama MCQ | FT',
    'jallama_bsl_xpl': 'Llama XPL | BSL',
    'jallama_ft_xpl': 'Llama XPL | FT'
}


names_experiments= {
    'fw0_exp0': 'Exp0',
    'fw1_exp1_G': 'Exp1.G',
    'fw1_exp1_G': 'Exp1.GxE',
    'fw2_exp2': 'Exp2.Prompt2',
    'fw2_exp3': 'Exp2.Prompt3',
    'fw2_exp4': 'Exp2.Prompt4',
    'gpt_bsl_mcq': 'Exp3 GPT MCQ | BSL',
    'gpt_ft_mcq': 'Exp3 GPT MCQ | FT',
    'gpt_bsl_xpl': 'Exp3 GPT XPL | BSL',
    'gpt_ft_xpl': 'FExp3T GPT XPL | FT',
    'jallama_bsl_mcq': 'Exp3 Llama MCQ | BSL',
    'jallama_ft_mcq': 'Exp3 Llama MCQ | FT',
    'jallama_bsl_xpl': 'Exp3 Llama XPL | BSL',
    'jallama_ft_xpl': 'Exp3 Llama XPL | FT'
}