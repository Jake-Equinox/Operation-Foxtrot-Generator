import streamlit as st

class StreamLit:
    @staticmethod
    def mainPage():
        st.title("Foxtrot Quote Generator 🦊")

        with st.sidebar:
            numOfShirt = st.number_input("How many shirts?", value = 20)
            cusSupply = st.radio("Is the customer supplying the garment?", ['No', 'Yes'])

            garmentCost = 0
            if cusSupply == 'No':
                garmentCost = st.number_input("How much is each garment?")
            featuredArtist = st.radio("Has the customer completed a Featured Artist run?", ['No', 'Yes'])
            numOfColour = st.slider("How many colours are present?", max_value=3)
            whitePrint = st.radio("Is white a colour?", ['No','Yes'])

            whiteQuantity = None
            if whitePrint == 'Yes':
                whiteQuantity = st.slider("How many shirts require white ink?", max_value= numOfShirt)

            largeGraphic = st.radio("Is the print a large graphic (greater than 14.8 (W) x 21.0 (H) cm", ['No', 'Yes'])
            screens = st.slider("How many screens to be made?", max_value=5)
            addOns = st.multiselect("Are there any add ons?", options=['Two Sides', 'Puff Print', 'Neck Prints', 'Outsourced Labels'])

        w, g, c, s, addOnTotal, initialEquation, equation, discount = StreamLit.calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour,
                            whitePrint, whiteQuantity, largeGraphic, screens, addOns)

        if numOfShirt == 0:
            st.error("Please complete sidebar before continuing!")
        else:
            st.write("")
            StreamLit.printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, w, g, c, s, addOnTotal, initialEquation, equation, discount)

    @staticmethod
    def calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour,
                            whitePrint, whiteQuantity, largeGraphic, screens, addOns):
        
        shirt_prices = {
            "below20": 12,
            "20_49": 7,
            "50_99": 5.50,
            "100_249": 4,
            "250_plus": 3
        }

        # Cost of Screens
        s = 0
        if screens == 1:
            s = 50
        elif screens == 2:
            s = 80
        elif screens == 3:
            s = 100
        elif screens >= 4:
            s = (screens * 30)

        # Cost of large graphic
        g = 0
        if largeGraphic == 'Yes':
            g = 0.5

        # Cost of the number of colours
        c = 0
        if numOfColour > 1:
            c = numOfColour

        # Cost of white ink
        w = 0
        if whitePrint:
            w = c + 1

        # Cost of extras
        addOnTotal = 0
        if 'Puff Print' in addOns:
            addOnTotal += 1
        if 'Neck Prints' in addOns:
            addOnTotal += 3
        if 'Outsourced Labels' in addOns:
            addOnTotal += 1.5
        if 'Two Sides' in addOns:
            addOnTotal += 2

        # ! Equation
        equation = 0
        if whitePrint == 'Yes':
            if numOfShirt < 20:
                equation = int((numOfShirt * shirt_prices["below20"]) +
                            (numOfShirt * addOnTotal) +
                            ((numOfShirt - int(whiteQuantity)) * c) +
                            int((whiteQuantity) * w) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 20 <= numOfShirt < 50:
                equation = int((numOfShirt * shirt_prices["20_49"]) +
                            (numOfShirt * addOnTotal) +
                            ((numOfShirt - int(whiteQuantity)) * c) +
                            int((whiteQuantity) * w) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 50 <= numOfShirt < 100:
                equation = int((49 * shirt_prices["20_49"] + (numOfShirt - 49) * shirt_prices["50_99"]) +
                            (numOfShirt * addOnTotal) +
                            ((numOfShirt - int(whiteQuantity)) * c) +
                            int((whiteQuantity) * w) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 100 <= numOfShirt < 250:
                equation = int((49 * shirt_prices["20_49"] + 50 * shirt_prices["50_99"] + (numOfShirt - 99) * shirt_prices["100_249"]) +
                            (numOfShirt * addOnTotal) +
                            ((numOfShirt - int(whiteQuantity)) * c) +
                            int((whiteQuantity) * w) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            else:
                equation = int((49 * shirt_prices["20_49"] + 50 * shirt_prices["50_99"] + 150 * shirt_prices["100_249"] + (numOfShirt - 249) * shirt_prices["250_plus"]) +
                            (numOfShirt * addOnTotal) +
                            ((numOfShirt - int(whiteQuantity)) * c) +
                            int((whiteQuantity) * w) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
        else:
            if numOfShirt < 20:
                equation = int((numOfShirt * (shirt_prices["below20"] + c)) +
                            (numOfShirt * addOnTotal) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 20 <= numOfShirt < 50:
                equation = int((numOfShirt * (shirt_prices["20_49"] + c)) +
                            (numOfShirt * addOnTotal) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 50 <= numOfShirt < 100:
                equation = int((49 * (shirt_prices["20_49"] + c)) + ((numOfShirt - 49) * (shirt_prices["50_99"] + c)) +
                            (numOfShirt * addOnTotal) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            elif 100 <= numOfShirt < 250:
                equation = int((49 * (shirt_prices["20_49"] + c) + 50 * (shirt_prices["50_99"] + c) + (numOfShirt - 99) * (shirt_prices["100_249"] + c)) +
                            (numOfShirt * addOnTotal) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))
            else:
                equation = int((49 * (shirt_prices["20_49"] + c) + 50 * (shirt_prices["50_99"] + c) + 150 * (shirt_prices["100_249"] + c) +
                            (numOfShirt - 249) * (shirt_prices["250_plus"] + c)) +
                            (numOfShirt * addOnTotal) +
                            (numOfShirt * g) + (s) + (numOfShirt * garmentCost))

        initialEquation = equation
        discount = 0
        if featuredArtist == 'Yes':
            discount = ((10/100) * equation)
            equation = equation - discount

        return w, g, c, s, addOnTotal, initialEquation, equation, discount

    @staticmethod
    def printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, w, g, c, s, addOnTotal, initialEquation, equation, discount):
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Summary"):
                st.write(f"Number of Shirts: {numOfShirt:<10}")
                st.write(f"Returning Artist: {featuredArtist == 'Yes'!s:<10}")
                st.write(f"Garment Cost: ${garmentCost:<10}")
                st.write(f"Large Graphic:    {g == 0.5!s:<10}")
                st.write(f"Total AddOns:     ${addOnTotal:<10}")
                st.write(f"Cost of Colours:  ${c:<10}")
                st.write(f"Cost of Screens:  ${s:<10}")
                st.write(f"Before Discount:  ${initialEquation:<10}")
                st.write(f"Discount Amount:  ${round(discount, 2):<10}")
                st.write(f"Cost to Customer: ${equation:<10}")
                st.write(f"Cost per Shirt:   ${round(equation/numOfShirt, 2):<10}")
                st.write(f"Foxtrot's Profit: ${(equation - (numOfShirt * garmentCost)):<10}")

        with col2:
            with st.expander("To Customer"):
                st.write(f"Number of Shirts: {numOfShirt:<10}")
                st.write(f"Cost of Colours:  ${c:<10}")
                st.write(f"Cost of Screens:  ${s:<10}")
                st.write(f"Total AddOns:     ${addOnTotal:<10}")
                st.write(f"Before Discount:  ${initialEquation:<10}")
                st.write(f"Discount Amount:  ${round(discount, 2):<10}")
                st.write(f"Cost to Customer: ${equation:<10}")
                st.write(f"Cost per Shirt:   ${round(equation/numOfShirt, 2):<10}")


def main():
    StreamLit.mainPage()


if __name__ == "__main__":
    main()
