import streamlit as st
import pandas as pd
import random


def authenticate():
    password_input = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Prosseguir"):
        if password_input == st.secrets.PASSWORD:
            st.session_state.autenticated = True
            return True
        else:
            st.error("Senha incorreta. Acesso negado ⛔!")
    return False


# Carregar o arquivo Excel
@st.cache_data
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df1 = xls.parse(xls.sheet_names[0])
    df2 = xls.parse(xls.sheet_names[1])
    return df1, df2


# Sortear números e stands únicos para cada área
# def sort_numbers_and_stands(df2):
#     # Agrupar o DataFrame 2 por área e gerar uma lista de stands para cada área
#     grouped_by_area = df2.groupby("Area")["Stand"].apply(list).to_dict()

#     # Embaralhar a ordem dos stands em cada área
#     for area in grouped_by_area:
#         random.shuffle(grouped_by_area[area])

#     return grouped_by_area


# Sortear stands únicos para cada área
def sort_stands(df2):
    stands_by_area = {}

    # Agrupar os dados por área
    grouped_by_area = df2.groupby("Área")

    for area, group in grouped_by_area:
        stands = list(group["Stand"])
        random.shuffle(stands)
        stands_by_area[area] = list(stands)

    return stands_by_area


# Associar stands sorteados às empresas
def assign_stands(df1, stands_by_area):
    assigned_stands = []

    for _, row in df1.iterrows():
        area = row["Área pretendida"]
        if area in stands_by_area and stands_by_area[area]:
            stand = stands_by_area[area].pop(0)
            assigned_stands.append(stand)
        else:
            assigned_stands.append(None)

    # print(f"Assigned Stands: {assigned_stands}")

    return assigned_stands


st.set_page_config(
    layout="centered", page_title="Prowein 2024", page_icon="assets/logo_ivdp.png"
)


def inject_custom_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style> {f.read()}</style>", unsafe_allow_html=True)


inject_custom_css()


# Função principal
def main():
    st.image("assets/prowein.png")

    st.title("Sorteio dos Stands para a Prowein 2024")

    if "autenticated" not in st.session_state:
        st.session_state.autenticated = False

    # Adicione uma autenticação simples
    if not st.session_state.autenticated:
        if not authenticate():
            st.stop()  # Interrompe a execução para que o restante do código não seja processado

    # st.markdown("Sorteio dos Stands para a __Prowein 2024__")

    # Carregar o arquivo Excel
    file_path = st.file_uploader(
        "Carregar ficheiro Excel com os dados:", type=["xls", "xlsx"]
    )

    # Adicionar uma flag para verificar se o botão foi pressionado
    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = False

    colL, colR = st.columns([4, 1])
    if file_path is not None:
        df1, df2 = load_data(file_path)

        # Mostrar os dados carregados
        colL.write("Empresas:")
        colR.write("Stands:")
        # Esconder a coluna de index (números de linha) ao exibir o DataFrame
        colL.dataframe(df1, hide_index=True)
        colR.dataframe(df2, hide_index=True)

        # Adicionar um botão para realizar o sorteio
        # Adicionar um botão para realizar o sorteio (desabilitado se já foi pressionado)
        if not st.session_state.button_pressed:
            if st.button("Realizar Sorteio 🎲"):
                # Sortear números para cada área
                # Sortear números e stands para cada área
                stands_by_area = sort_stands(df2)
                # print(numbers_and_stands_by_area)

                # Associar números e stands sorteados às empresas
                assigned_stands = assign_stands(df1, stands_by_area)

                # Adicionar os números e stands às empresas no DataFrame original
                # df1["Numero"] = assigned_numbers
                df1["Stand"] = assigned_stands
                st.session_state.dfinal = df1
                # Atualizar a flag para indicar que o botão foi pressionado
                st.session_state.button_pressed = True
                # Rerun experimental para atualizar a interface gráfica
                st.rerun()

        if st.session_state.button_pressed:
            # Exibir os resultados
            st.write("Resultado do Sorteio:")

            st.dataframe(
                st.session_state.dfinal, use_container_width=True, hide_index=True
            )

        # Adicione o "Footer" aqui
        st.markdown("---")
        st.markdown("© 2024 IVDP. Todos os direitos reservados.")
    # else:
    #     st.stop()  # Interrompe a execução para que o restante do código não seja processado


if __name__ == "__main__":
    main()
