import streamlit as st

class StreamLit:

    def mainPage():
        st.title("Foxtrot Quote Generator 🦊")

        with st.sidebar:
            numOfShirt = st.slider("How many shirts?", max_value= 250)
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

            twoSides = st.radio("Is there a backgraphic?", ['No', 'Yes'])
            
            backNum = None
            if twoSides == 'Yes':
                backNum = st.slider("How many shirts require backgraphics?", max_value=numOfShirt)
            
            largeGraphic = st.radio("Is the print a large graphic (greater than 14.8 (W) x 21.0 (H) cm", ['No', 'Yes'])
            screens = st.slider("How many screens to be made?", max_value=5)
            addOns = st.multiselect("Are there any add ons?", options=['Puff Print', 'Neck Prints', 'Outsourced Labels'])        
        

        x, w, g, c, s, addOnTotal, initialEquation, equation, discount = Utilities.calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour, 
                            whitePrint, whiteQuantity, twoSides, backNum, largeGraphic, screens, addOns)


        if numOfShirt == 0:
            st.error("Please complete sidebar before continuing!")
        else:
            st.write("")
            Utilities.printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, x, w, g, c, s, addOnTotal, initialEquation, equation, discount)

        

class Utilities:

    def calculateContractJob(cusSupply, featuredArtist, numOfShirt, garmentCost, numOfColour, 
                            whitePrint, whiteQuantity, twoSides, backNum, largeGraphic, screens, addOns):
        
        shirtBelow20 = 12
        shirt20_49 = 7
        shirt50_99 = 5.50
        shirt100_249 = 4
        shirt250_plus = 3
        
        
        twoSidesCost = 0
        if twoSides == 'Yes':
            twoSidesCost = 2

        x = 0
        if cusSupply == 'No':
            if numOfShirt < 20:
                print("Please note there is a minimum of 20 required!")
                x = (shirtBelow20 + twoSidesCost) + garmentCost
            elif numOfShirt >= 20 and numOfShirt <= 49:
                x = (shirt20_49 + twoSidesCost) + garmentCost
            elif numOfShirt >= 50 and numOfShirt <= 99:
                x = (shirt50_99 + twoSidesCost) + garmentCost
            elif numOfShirt >= 100 and numOfShirt <= 249:
                x = (shirt100_249 + twoSidesCost) + garmentCost
            elif numOfShirt >= 250:
                x = (shirt250_plus + twoSidesCost) + garmentCost
        elif cusSupply == 'Yes':
            if numOfShirt < 20:
                print("Please double check with customer about printing less than 20!")
                x = (shirtBelow20 + twoSidesCost)
            elif numOfShirt >= 20 and numOfShirt <= 49:
                x = (shirt20_49 + twoSidesCost) 
            elif numOfShirt >= 50 and numOfShirt <= 99:
                x = (shirt50_99 + twoSidesCost) 
            elif numOfShirt >= 100 and numOfShirt <= 249:
                x = (shirt100_249 + twoSidesCost) 
            elif numOfShirt >= 250:
                x = (shirt250_plus + twoSidesCost)        
        s = 0
        if screens == 1:
            s = 50
        elif screens == 2:
            s = 80
        elif screens == 3:
            s = 100
        elif (screens >= 4):
            s = (screens * 30)
        
        g = 0
        if largeGraphic == 'Yes':
            g = 0.5
        
        c = 0
        if numOfColour > 1:
            c = numOfColour
        
        w = 0
        if whitePrint:
            w = c + 0.5
        
        addOnTotal = 0
        if 'Puff Print' in addOns:
            addOnTotal += 1
        if 'Neck Prints' in addOns:
            addOnTotal += 3
        if 'Outsourced Labels' in addOns:
            addOnTotal += 1.5
        

        if whitePrint == 'Yes':
            equation = int((numOfShirt * x) + \
                        (numOfShirt * addOnTotal) + \
                        ((numOfShirt - int(whiteQuantity)) * c) + \
                        int((whiteQuantity) * w) + \
                        (numOfShirt * g) + (s))
            initialEquation = equation
            discount = 0
            if featuredArtist == 'Yes':
                discount = ((10/100) * equation)
                equation = equation - discount
        else:
            equation = int((numOfShirt * (x + c)) + (numOfShirt *
                                                    addOnTotal) + (numOfShirt * g) + (s))
            initialEquation = equation
            discount = 0
            if featuredArtist == 'Yes':
                discount = ((10/100) * equation)
                equation = equation - discount
        
        return x, w, g, c, s, addOnTotal, initialEquation, equation, discount

    def printOut(cusSupply, featuredArtist, numOfShirt, garmentCost, x, w, g, c, s, addOnTotal, initialEquation, equation, discount):

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Summary"):
                st.write(f"Number of Shirts: {numOfShirt:<10}")
                st.write(f"Returning Artist: {featuredArtist == 'Yes'!s:<10}")
                st.write(f"Shirt Cost Price: ${x:<10}")
                st.write(f"Large Graphic:    {g == 0.5!s:<10}")
                st.write(f"Total AddOns:     ${addOnTotal:<10}")
                st.write(f"Cost of Colours:  ${c:<10}")
                st.write(f"Cost of Screens:  ${s:<10}")
                st.write(f"Before Discount:  ${initialEquation:<10}")
                st.write(f"Discount Amount:  ${round(discount, 2):<10}")
                st.write(f"Cost to Customer: ${equation:<10}")
                st.write(f"Cost per Shirt:   ${round(equation/numOfShirt, 2):<10}")
                if cusSupply == 'Yes':
                    st.write(
                        f"Foxtrot's Profit: ${(equation - (numOfShirt * garmentCost)):<10}")
                else:
                    st.write(f"Foxtrot's Profit: ${round(equation, 2):<10}")

        
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