import streamlit as st
import pandas as pd
import random
from openpyxl import Workbook
from openpyxl.styles import Font
from io import BytesIO


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


# Função para exportar DataFrame para Excel com formatação personalizada
def export_to_excel(df):
    # Cria um objeto BytesIO para armazenar o Excel em memória
    with BytesIO() as excel_buffer:
        try:
            # Cria um objeto Workbook do openpyxl
            wb = Workbook()

            # Cria uma planilha no Workbook
            ws = wb.active

            # Adiciona os dados do DataFrame à folha
            ws.append(list(df.columns))  # Adiciona a primeira linha com cabeçalhos
            for r_idx, row in enumerate(df.itertuples(), start=2):
                ws.append(row[1:])  # Ignora o índice do DataFrame

            # Formatação personalizada
            header_font = Font(bold=True)
            for cell in ws[1]:
                cell.font = header_font

            # Autoajuste de largura de coluna
            for column in ws.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                ws.column_dimensions[column[0].column_letter].width = adjusted_width

            ws.title = "Sorteio"

            # Gravar o ficheiro Excel no BytesIO
            wb.save(excel_buffer)

            # Retornar os bytes do Excel em base64
            return excel_buffer.getvalue()

        except Exception as e:
            # Tratar exceções ao salvar o Workbook
            print(f"Erro ao gravar o Workbook: {e}")
            return None


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

        st.image("assets/prowein-exhibition-map.jpg")

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
            b64_data = export_to_excel(st.session_state.dfinal)

            if b64_data:
                st.download_button(
                    label="Clique aqui para fazer download do sorteio ✅",
                    data=b64_data,
                    file_name="resultado_sorteio.xlsx",
                    key="download_excel_button",
                    help="Clique para descarregar o ficheiro Excel.",
                    on_click=None,  # Você pode adicionar uma função de callback aqui, se necessário
                    args=None,
                    kwargs=None,
                )
            else:
                st.warning("Houve um problema ao gerar o ficheiro Excel.")

        # Adicione o "Footer" aqui
        st.markdown("---")
        st.markdown("© 2024 IVDP. Todos os direitos reservados.")
    # else:
    #     st.stop()  # Interrompe a execução para que o restante do código não seja processado


if __name__ == "__main__":
    main()
